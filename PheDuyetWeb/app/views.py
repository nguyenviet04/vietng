from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import messages framework
from .forms import CustomUserCreationForm, CreditApplicationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CreditApplication
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
import os

#Tải mô hinh
decision_tree_model = None # Luôn khởi tạo biến trước
MODEL_PATH = os.path.join(settings.BASE_DIR, 'model', 'decision_tree_model.pkl')
try:
    decision_tree_model = joblib.load(MODEL_PATH)
    print("Tải mô hình 'decision_tree_model.pkl' thành công!")
except FileNotFoundError:
    print(f"CẢNH BÁO: Không tìm thấy file mô hình tại '{MODEL_PATH}'. Ứng dụng sẽ chạy ở chế độ demo.")
except Exception as e:
    print(f"LỖI: Có vấn đề khi tải mô hình: {e}")
def home(request):
    return render(request, 'credit_app/home.html')
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công! Vui lòng điền thông tin để đăng ký tín dụng.')
            return redirect('credit_application')
        else:
            messages.error(request, 'Có lỗi khi đăng ký. Vui lòng kiểm tra lại thông tin.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'credit_app/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng trở lại, {username}!')
                return redirect('credit_application')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        else:
            messages.error(request, "Có lỗi khi đăng nhập. Vui lòng kiểm tra lại thông tin.")
    else:
        form = AuthenticationForm()
    return render(request, 'credit_app/login.html', {'form': form})
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công.')
    return redirect('home')
# --- ÁNH XẠ (MAPPING) TỪ DỮ LIỆU FORM SANG SỐ CHO MODEL ---
# Tạo các dictionary này để chuyển đổi dữ liệu từ form sang dạng số mà model hiểu
INDUSTRY_MAP = {k: v for v, k in enumerate(CreditApplication.IndustryChoices.values)}
ETHNICITY_MAP = {k: v for v, k in enumerate(CreditApplication.EthnicityChoices.values)}
CITIZEN_MAP = {k: v for v, k in enumerate(CreditApplication.CitizenChoices.values)}


@login_required
def credit_application(request):
    if request.method == 'POST':
        form = CreditApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user

            # Lấy dữ liệu đã được làm sạch từ form
            data = form.cleaned_data

            # --- CHUẨN BỊ DỮ LIỆU ĐÚNG THỨ TỰ VÀ ĐÚNG ĐỊNH DẠNG CHO MODEL ---
            feature_list = [
                int(data['gender']),
                data['age'],
                data['debt'],
                int(data['married']),
                int(data['bank_customer']),
                INDUSTRY_MAP[data['industry']],  # Chuyển đổi Industry
                ETHNICITY_MAP[data['ethnicity']],  # Chuyển đổi Ethnicity
                data['years_employed'],
                1 - int(data['prior_default']),
                int(data['employed']),
                data['credit_score'],
                int(data['drivers_license']),
                CITIZEN_MAP[data['citizen']],  # Chuyển đổi Citizen
                int(data['zip_code']),
                data['income']
            ]

            # Chuyển thành numpy array để dự đoán
            features_array = np.array(feature_list).reshape(1, -1)

            # --- Phần dự đoán (giữ nguyên logic cũ) ---
            if decision_tree_model:
                try:
                    prediction = decision_tree_model.predict(features_array)[0]
                    if prediction == 1:
                        application.approval_result = "Phê duyệt"
                        messages.success(request, 'Đơn đăng ký của bạn đã được PHÊ DUYỆT!')
                    else:
                        application.approval_result = "Từ chối"
                        messages.warning(request, 'Đơn đăng ký của bạn đã bị TỪ CHỐI.')
                except Exception as e:
                    application.approval_result = "Lỗi dự đoán"
                    messages.error(request, f'Có lỗi xảy ra khi dự đoán: {e}')
            else:
                # Logic demo
                application.approval_result = "Từ chối (Demo)"
                messages.info(request, 'Đây là kết quả demo do mô hình chưa sẵn sàng.')

            application.save()
            return redirect('approval_result')
    else:
        form = CreditApplicationForm()
    return render(request, 'credit_app/credit_application.html', {'form': form})
def approval_result(request):
    """
    Hiển thị kết quả của đơn đăng ký gần nhất của người dùng.
    """
    try:
        latest_application = CreditApplication.objects.filter(user=request.user).latest('created_at')
    except CreditApplication.DoesNotExist:
        latest_application = None
    return render(request, 'credit_app/approval_result.html', {'application': latest_application})

@login_required
def my_profile(request):
    """
    Hiển thị thông tin người dùng và lịch sử các đơn đăng ký đã nộp.
    """
    user_applications = CreditApplication.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'credit_app/my_profile.html', {'applications': user_applications})
