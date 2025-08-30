from django.db import models
from django.contrib.auth.models import User

class CreditApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")

    class IndustryChoices(models.TextChoices):
        COMMUNICATION_SERVICES = 'CommunicationServices', 'Dịch vụ Viễn thông'
        CONSUMER_DISCRETIONARY = 'ConsumerDiscretionary', 'Tiêu dùng không thiết yếu'
        CONSUMER_STAPLES = 'ConsumerStaples', 'Tiêu dùng thiết yếu'
        EDUCATION = 'Education', 'Giáo dục'
        ENERGY = 'Energy', 'Năng lượng'
        FINANCIALS = 'Financials', 'Tài chính'
        HEALTHCARE = 'Healthcare', 'Y tế'
        INDUSTRIALS = 'Industrials', 'Công nghiệp'
        INFORMATION_TECHNOLOGY = 'InformationTechnology', 'Công nghệ thông tin'
        MATERIALS = 'Materials', 'Vật liệu'
        REAL_ESTATE = 'RealEstate', 'Bất động sản'
        RESEARCH = 'Research', 'Nghiên cứu'
        TRANSPORT = 'Transport', 'Giao thông Vận tải'
        UTILITIES = 'Utilities', 'Tiện ích'

    class EthnicityChoices(models.TextChoices):
        ASIAN = 'Asian', 'Châu Á'
        BLACK = 'Black', 'Da đen'
        LATINO = 'Latino', 'Latin'
        WHITE = 'White', 'Da trắng'
        OTHER = 'Other', 'Khác'

    class CitizenChoices(models.TextChoices):
        BY_BIRTH = 'ByBirth', 'Theo nơi sinh'
        BY_OTHER_MEANS = 'ByOtherMeans', 'Theo cách khác'
        TEMPORARY = 'Temporary', 'Tạm thời'

    gender = models.BooleanField(verbose_name="Giới tính (Nam)", help_text="Chọn nếu là Nam")
    age = models.FloatField(verbose_name="Tuổi")
    debt = models.FloatField(verbose_name="Nợ")
    married = models.BooleanField(verbose_name="Đã kết hôn")
    bank_customer = models.BooleanField(verbose_name="Là khách hàng ngân hàng")
    industry = models.CharField(max_length=50, choices=IndustryChoices.choices, verbose_name="Ngành công nghiệp")
    ethnicity = models.CharField(max_length=20, choices=EthnicityChoices.choices, verbose_name="Sắc tộc")
    years_employed = models.FloatField(verbose_name="Số năm làm việc")
    prior_default = models.BooleanField(verbose_name="Có nợ xấu trong quá khứ")
    employed = models.BooleanField(verbose_name="Có việc làm")
    credit_score = models.IntegerField(verbose_name="Điểm tín dụng")
    drivers_license = models.BooleanField(verbose_name="Có giấy phép lái xe")
    citizen = models.CharField(max_length=20, choices=CitizenChoices.choices, verbose_name="Tình trạng công dân")
    zip_code = models.CharField(max_length=10, verbose_name="Mã bưu điện")
    income = models.IntegerField(verbose_name="Thu nhập")

    # --- Trường kết quả ---
    approval_result = models.CharField(max_length=20, blank=True, null=True, verbose_name="Kết quả phê duyệt")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đơn đăng ký tín dụng"
        verbose_name_plural = "Các đơn đăng ký tín dụng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn của {self.user.username} - {self.created_at.strftime('%d/%m/%Y')}"