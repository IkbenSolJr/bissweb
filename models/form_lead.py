# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import requests
from odoo import http
from odoo.http import request


class FormLead(models.Model):
    _name = 'formreview.lead'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'lead_form_id'
    # Field Public:
    is_public_form = fields.Boolean(
        string='Là Form Công Khai',
        default=False,
        help='Đánh dấu lead được tạo từ form công khai',
        tracking=True  # Để track thay đổi trong chatter
    )
    lead_form_id = fields.Many2one('crm.lead', string="Họ và Tên")
    close_form = fields.Boolean(string="Khóa Form", default= False)
    # Phan co van
    ngayguiform = fields.Date(string="Ngày đặt hẹn gửi form",default=lambda self: fields.Datetime.now())  
    covanluatsu = fields.Char('Cố vấn và Luật sư')
    covanct  = fields.Char('Cố vấn chương trình')
    ketqua = fields.Char('Kết quả khách hàng chọn')
    ngayduyet = fields.Date(string="Ngày duyệt")
    # Phan duong dơn
    # name = fields.Char(string="Họ và Tên")
    quoctich = fields.Char(string="Quốc tịch")
    gioitinh = fields.Selection([
        ('nam', 'Nam'),
         ('nu', 'Nữ')       
    ], string='Giới tính')
    namsinhnd = fields.Char(string="Ngày tháng năm sinh")
    email = fields.Char(string="Địa chỉ Email")
    phone = fields.Char(string="Số điện thoại")
    hkthuongtru = fields.Text(string="Hộ khẩu thường trú")
    noio = fields.Text(string="Nơi ở hiện tại")
    tinhtranghn = fields.Text(string="Tình trạng hôn nhân (Độc thân/ Đã có gia đình/ Đã ly hôn)")
    # -----Nguyện vọng của đương đơn ----  
    nguyenvongdd = fields.Text(string="Nguyện vọng của đương đơn")
    nhucau = fields.Text(string="Hình thức mong muốn (Du lịch, du học, lao động, định cư, đầu tư,..)")
    visa = fields.Selection([('482', '482'),('482dama', '482 DAMA'),('462', '462'),('500', '500'),('600', '600'),('186', '186'),('186dama', '186 DAMA'),('403', '403'),('407', '407'),('494', '494'),('dubai', 'Dubai'),('caworkpermit', 'Canada Work Permit'),('ca', 'Canada'),('uc', 'Úc'),('nz', 'NZ'),('laodong', 'Lao động'),('dulich', 'Du lịch'),('khac', 'Khác')], string="Loại Visa",track_visibility='onchange',default=False)
    quocgiabook = fields.Selection([('uc', 'Úc'),
                                ('canada', 'Canada'),
                                ('ireland', 'Ireland')], 
                                string="Quốc gia Book", default=False)
    nghebooking = fields.Selection([('bep', 'Bếp'),
                                ('farm', 'Farm'),
                                ('thit', 'Thịt'),
                                ('holy', 'Hộ lý'),
                                ('xaydung', 'Xây dựng'),
                                ('chebienthit', 'Chế biến thịt'),
                                ('oto', 'Ô tô'),
                                ('adgecare', 'Aged care'),
                                ('hair', 'Hair'),
                                ('thohancokhi', 'Thợ hàn, Cơ khí'),
                                ('nhahang', 'Nhà hàng khách sạn'),
                                ('thomoc', 'Thợ mộc'),
                                ('tapvu', 'Tạp vụ'),
                                ('ketoan', 'Kế toán'),
                                ('duhoc', 'Du học'),
                                ('nvkho','Nhân viên kho'),
                                ('thone','Thợ nề'),
                                ('nuoichongthuysan','Nhân viên nuôi trồng thủy hải sản'),
                                ('nongtraisx','Nhân viên nông trại sản xuất'), 
                                ('vanhanhmaynn','Nhân viên vận hành máy móc nông nghiệp'),
                                ('suathanvooto','Sửa chữa thân vỏ ô tô'), 
                                ('thohan','Thợ ốp lát, Thợ hàn'), 
                                ('spalamdep','Quản lý Spa làm đẹp'), 
                                ('thokythuat','Thợ kỹ thuật'), 
                                ('thodienlanh','Thợ điện lạnh'),
                                ('kientrucsu','Kiến trúc sư'), 
                                ('nvbanle','Nhân viên bán lẻ'), 
                                ('quantrictvada','Quản trị viên chương trình và dự án'),
                                ('tuvanmkt','Quản lý nhân viên tư vấn và marketing'), 
                                ('laptrinhvien','Lập trình viên'),
                                ('kysumang','Kỹ sư mạng'), 
                                ('thokinh','Thợ làm kính'),
                                ('bsygiadinh','Bác sỹ gia đình'), 
                                ('gvmamnon','Giáo viên mầm non'),
                                ('duhoc','Quản lý dự án xây dựng'),
                                 #Bosung
                                ('beautytherapist', 'Beauty Therapist'),
                                ('bocnoithat', 'Thợ bọc nội thất'),
                                #
                                ('khac', 'Nghề khác')], 
                                string="Nghề booking", default=False)
    nguoithan = fields.Text(string="Ứng viên có người thân hỗ trợ công việc/ nhà ở tại quốc gia mình mong muốn hay không?")
    # -----Năng lục ứng viên(Đương đơn)----
    chungchitaynghe = fields.Char(string="Chứng chỉ tay nghề/nếu có (Ghi rõ thời gian khóa học bao nhiêu tháng – năm tốt nghiệp)")
    bangcap = fields.Selection([('tieuhoc', 'Tiểu học'),
                                ('thcs', 'THCS'),
                                ('thpt', 'THPT'),
                                ('trungcap', 'Trung cấp'),
                                ('caodang', 'Cao đẳng'),
                                ('daihoc', 'Đại học')], 
                                string="Bằng cấp cao nhất từng có", default=False)
    chuyennganh = fields.Char(string="Chuyên môn ngành nghề (theo bằng cấp)")
    #truongcap = fields.Char(string="Trường cấp bằng")
    namtotnghiep = fields.Char(string="Năm tốt nghiệp")
    # ----Tiếng Anh ----
    tienganh = fields.Selection([('khong', 'Không'),
                                ('coban', 'Cơ bản'),
                                ('giaotiep', 'Giao tiếp'),
                                ('ie34pte23', 'Ielts 3.0-4.0/ PTE 23+'),
                                ('ie45pte29', 'Ielts 4.0-5.0 /PTE 29+'),
                                ('ie56pte36', 'Ielts 5.0-6.0 / PTE 36+'),
                                ('ie6pte46', 'Ielts trên 6.0 / PTE 46+')], 
                                string="Trình độ tiếng anh", default=False)
    chungchita = fields.Char(string="Bằng cấp tiếng anh và điểm số (nếu có)")
    namcapccta = fields.Char(string="Năm cấp bằng")
    # ----Kinh nghiêm làm việc 18t đến nay----
    congviecht = fields.Text(string="Công việc hiện tại")
    tendoanhnghiepht = fields.Text(string="Tên công ty và lĩnh vực hoạt động")
    thoigianlamht = fields.Char(string="Thời gian công tác")
    kinhnghiemht = fields.Text(string="Chứng minh kinh nghiệm")  
    # ----Kinh nghiêm làm việc 5 đến 10 năm trước----
    congviectruocday = fields.Text(string="Công việc trước đây")
    tendoanhnghiep = fields.Text(string="Tên công ty và lĩnh vực hoạt động")
    thoigianlam = fields.Char(string="Thời gian công tác")
    kinhnghiem = fields.Text(string="Chứng minh kinh nghiệm")  
    # ----Tiểu sử di trú  ----
    capvisadulichvfs = fields.Text(string="Ứng viên đã từng được cấp hoặc bị từ chối visa du lịch trong khối VFS hay không?")
    capvisalaodongvfs = fields.Text(string="Ứng viên đã từng được cấp hoặc bị từ chối visa lao động trong khối VFS hay không?")
    capvisaqgkhac = fields.Text(string="Ứng viên đã từng được cấp hoặc bị từ chối visa du lịch/ lao động,.. trong các quốc gia khác hay không?")
    #caplaivisa = fields.Text(string="Đương đơn/gia đình có đang nộp/chờ kết quả visa không?")
    #tuchoivisagd = fields.Text(string="Bố/ mẹ/ anh chị em/Chồng con đã từng được cấp hoặc bị từ chối visa vào nước nào?")
    # ----Lý lịch tư pháp  ----
    phamphap = fields.Char(string="Đương đơn hoặc người thân gia đình đã từng bị phạt hoặc kết án về tội danh nào hay chưa?")
    suckhoe = fields.Text(string="Đương đơn có vấn đề về sức khỏe các bệnh truyền nhiễm ảnh hưởng đến vấn đề xuất nhập cảnh với visa lao động như: Viêm gan, Lao phổi, HIV,...")
    # ----Chứng minh từ tài chính gia đình Áp dụng Form Du học ----  
    #nguoitaitro_dh = fields.Char(string="Người bảo trợ tài chính (Ba, mẹ, người thân,…)")
    #luongthangdd_dh = fields.Char(string="Lương thực nhận hàng tháng của đương đơn")
    #luongthangpt_dh = fields.Char(string="Lương thực nhận hàng tháng của người phụ thuộc (nếu có)")
    #thunhapbds_dh = fields.Char(string="Thu nhập khác từ cho thuê nhà đất, xe hơi, tàu, thuyền; đầu tư chứng khoán,...")
    sotk_dh  = fields.Char(string="Sổ tiết kiệm (Giá trị tài sản, thời hạn sổ tiết kiệm)")
    tsbds_dh = fields.Char(string="Tài sản nhà/ đất và tổng giá trị theo thị trường (Đứng tên đương đơn hoặc người phụ thuộc)")
    # ----Chứng minh tài chính đương đơn/ Người phụ thuộc cá nhân----  
    #luongthang = fields.Char(string="Lương thực nhận hàng tháng của đương đơn")
    #luongthang_pt = fields.Char(string="Lương thực nhận hàng tháng của người phụ thuộc (nếu có)")
    #thunhapbds = fields.Char(string="Thu nhập khác từ cho thuê nhà đất, xe hơi, tàu, thuyền; đầu tư chứng khoán,...")
    sotk  = fields.Char(string="Sổ tiết kiệm (Giá trị tài sản, thời hạn sổ tiết kiệm)")
    tsbds = fields.Char(string="Tài sản nhà/ đất và tổng giá trị theo thị trường (Đứng tên đương đơn hoặc người phụ thuộc)")
    # ----Chứng minh tài chính đương đơn/ Người phụ thuộc DOanh nghiep ----
    hinhthucdn = fields.Char(string="Hình thức doanh nghiệp hoạt động")
    dongthuedn = fields.Selection([
                            ('co', 'Có'),
                            ('khong', 'Không')       
                            ], string='Có đóng thuế đầy đủ hay không')
    giayphepkddn = fields.Selection([
                            ('co', 'Có'),
                            ('khong', 'Không')       
                            ], string='Có giấy phép kinh doanh hay không')  
    mst_webdn = fields.Char(string="Link website hoặc mã số thuế (nếu có)")
    thunhapbdsdn = fields.Char(string="Thu nhập khác từ cho thuê nhà đất, xe hơi, tàu, thuyền; đầu tư chứng khoán,...")
    sotkdn = fields.Char(string="Sổ tiết kiệm (Giá trị tài sản, thời hạn sổ tiết kiệm)")
    bdsdn = fields.Char(string="Tài sản nhà/ đất & tổng giá trị theo thị trường ")
    # ----Người phụ thuộc ----
    name_npt = fields.Char(string="Họ và tên (người phụ thuộc)")
    namsinh_npt = fields.Char(string="Ngày tháng năm sinh")
    bangcap_npt = fields.Char(string="Bằng cấp cao nhất từng có")
    cvht_npt = fields.Char(string="Công việc hiện tại")
    tienganh_npt = fields.Char(string="Trình độ tiếng Anh")

    link_ur = fields.Char(string='Links Form gửi đi', compute='_compute_lead_form_url')

    @api.depends('lead_form_id')
    def _compute_lead_form_url(self):
        for record in self:
            # Construct the URL dynamically for each lead
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            # record.link_ur = f'{base_url}/web#id={record.id}&view_type=form&model=crm.lead'
            record.link_ur = f'{base_url}/form_custumer/{record.id}'
            


    def action_open_custom_web_form(self):
             return {
            'type': 'ir.actions.act_url',
            'url': '/form_custumer/%d' % self.id,
            'target': 'new',
        }


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    form_lead_ids =  fields.One2many('formreview.lead','lead_form_id',string="Form Review")   
    form_count = fields.Integer(string="Count Form", compute='_compute_form_lead_count',store=True) 

    def _compute_form_lead_count(self):
        for rec in self:
            form_count = self.env['formreview.lead'].search_count([('lead_form_id', '=', rec.id)])
            rec.form_count = form_count 

    def action_view_form_lead(self):  
            return {
                'type': 'ir.actions.act_window',
                'name': 'View Form Lead',
                'res_model': 'formreview.lead',
                'domain': [('lead_form_id', '=', self.id)],
                'context': {'search_lead_form_id': self.id,
                            'default_lead_form_id': self.id,
                            'default_phone': self.phone,
                            'default_email': self.email_from,
                            'default_visa': self.visa,
                            },
                'view_mode': 'tree,form',
                'target': 'current',
            }