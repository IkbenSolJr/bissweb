# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import requests
import logging
from odoo import http
from odoo.http import request

# Set up a logger for this module
_logger = logging.getLogger(__name__)

class bissweb(models.Model):
    _name = 'crm.lead'
    _inherit = 'res.partner'
    _inherit = 'crm.lead'



    ngaynhap = fields.Date(string="Ngày nhập",default=lambda self: fields.Datetime.now())
    nhucau = fields.Char(string="Nhu cầu")
    trangthaidt = fields.Selection([
                                ('khongbatmay', 'Không bắt máy/Thuê bao (Lần 1)'),
                                ('khongbatmayhai', 'Không bắt máy/Thuê bao (Lần 2)'),
                                ('khongbatmayba', 'Không bắt máy/Thuê bao (Lần 3)'),
                                ('khongbatmaybon', 'Không bắt máy/Thuê bao (Lần 4)'),
                                ('khongbatmaynam', 'Không bắt máy/Thuê bao (Lần 5)'),
                                ('khongconhucau', 'Không có nhu cầu'),
                                ('hengoilai', 'Hẹn gọi lại'),
                                ('trungdata', 'Trùng data'),
                                ('saiso', 'Không kết nối dc/ Sai số DT/ SDT không đúng'),
                                ('thamgiapitching', 'Đồng ý tham gia pitching'),
                                ('daguitinzalokb', 'Đã gửi tin nhắn/Zalo kết bạn cho khách'),
                                ('khongdutaichinh', 'Tài chính yếu'),   
                                ('taichinhchuadu', 'Tài chính chưa đủ'), 
                                ('timhieuthem', 'Cần tìm hiểu thêm'),  
                                ('doituongdotuoilon', 'Lớn tuổi'),
                                ('doituongdungchamsoc', 'Dừng chăm sóc'),
                                ('doituongkhongphuhop', 'Đối tượng KH không phù hợp'),
                                ('doituongchamsoc', 'Đúng đối tượng, chăm sóc booking'),
                                ('lylichtpxau', 'Lý lịch tư pháp/Sức khỏe xấu'),
                                ('pitchingguithamdinh', 'KH đã gửi hồ sơ thẩm định'),
                                ('bopitching', 'Không tham gia pitching'),
                                ('thamgiareview', 'Đã tham gia trả kết quả thẩm định hồ sơ'),
                                ('guiemailofferkh', 'Đã gửi email offer cho KH'),
                                ('guiemailhd', 'Đã gửi email hợp đồng cho KH'),
                                ('thamgiadgenglish', 'Đã tham gia đánh giá Tiếng Anh'),
                                ('follownganhan', 'Follow ngắn hạn(dưới 1 tháng)'),
                                ('followdaihan', 'Follow dài hạn(từ 1 tháng trở lên)'),
                                ('deposit', 'Deposit'),
                                ('tiemnangkyhd', 'Tiềm năng ký hợp đồng'),    
                                ('dakyhdttmot', 'Ký hợp đồng - Đã thanh toán giai đoạn 1'),
                                ('ttlanhai', 'Ký hợp đồng - Đã thanh toán giai đoạn 2'),
                                ('daxeplopta', 'Đã xếp lớp Tiếng Anh'),
                                ('daxeplopdtn', 'Đã xếp lớp đào tạo nghề'),
                                ('daotaopv', 'Đào tạo phỏng vấn'),
                                ('quantambhpxkld', 'Quan tâm chương trình BHP / XKLĐ'),
                                ('khac', 'Khác')    
                                ],
                                string="Trạng thái KH",track_visibility='onchange',default=False)
    trinhdo = fields.Char(string="Trình độ")
    tienganh = fields.Char(string="Tiếng Anh")
    namsinh = fields.Char(string="Năm sinh")
    sinhnhat = fields.Date(string="Sinh nhật")
    noio = fields.Char(string="Nơi ở hiện tại")
    nghenghiep = fields.Char(string="Nghề nghiệp")
    taichinh = fields.Char(string="Tài chính")
    hopdong = fields.Char(string="Tình trạng HĐ")
    #visa = fields.Selection([('482', '482'),('482dama', '482 DAMA'),('462', '462'),('500', '500'),('600', '600'),('186', '186'),('186dama', '186 DAMA'),('403', '403'),('407', '407'),('494', '494'),('dubai', 'Dubai'),('caworkpermit', 'Canada Work Permit'),('ca', 'Canada'),('uc', 'Úc'),('nz', 'NZ'),('laodong', 'Lao động'),('dulich', 'Du lịch'),('khac', 'Khác')], string="Loại Visa",track_visibility='onchange',default=False)
    visa = fields.Selection([('482', '482'),
                             ('482dama', '482 DAMA'),
                             ('462', '462'),
                             ('500', '500'),
                             ('600', '600'),
                             ('186', '186'),
                             ('186dama', '186 DAMA'),
                             ('403', '403'),
                             ('407', '407'),
                             ('494', '494'),
                             ('dubai', 'Dubai'),
                             ('caworkpermit', 'Canada Work Permit'),
                             ('ca', 'Canada'),
                             ('uc', 'Úc'),
                             ('nz', 'NZ'),
                             ('laodong', 'Lao động'),
                             ('dulich', 'Du lịch'),
                             ('khac', 'Khác')], 
                             string="Loại Visa",track_visibility='onchange',default=False)
    danhgiakh = fields.Selection([('tiemnang', 'Tiềm năng'),
    ('khongtiemnang', 'Không tiềm năng'),('lenhopdongmau', 'Đã lên hợp đồng'),('hot', 'Hot'),('kyhd', 'Ký Hợp đồng')],string="Đánh giá KH",track_visibility='onchange',default=False)
    ngaychuyengiao = fields.Date(string='Ngày chuyển giao')
    nguondt = fields.Selection([('hotline', 'Hotline'),
                                ('hotlinemn', 'Hotline Miền Nam'),
                                ('hotlinemb', 'Hotline Miền Bắc'),
                                ('hotlinemt', 'Hotline Miền Trung'),
                                ('tiktok', 'Tiktok'),
                                ('gmail', 'Gmail'),
                                ('seeding', 'Seeding'),
                                ('tructieptaivanphong', 'Trực tiếp tại văn phòng'),
                                ('tunguoiquen', 'Từ người quen'),
                                ('chidaisy', 'Chị Daisy'),
                                ('facebook', 'Facebook Chính'),
                                ('facebooktichxanh', 'Facebook Tích Xanh'),
                                ('facebookads', 'Facebook Miền Trung'),
                                ('facebookmienbac', 'Facebook Miền Bắc'),
                                ('zalo', 'Zalo'),
                                ('website', 'Website'),
                                ('googleads', 'Google Ads'),                       
                                ('lhu', 'LHU'),
                                ('dsstraining', 'DSS Training'),
                                ('khgioithieu', 'KH giới thiệu'),
                                ('doitac', 'Đối tác'),
                                ('sukien', 'Sự kiện'),                                
                                ('nguonkhac', 'Nguồn khác')],
                                string="Nguồn data")
    adsdss = fields.Char(string="Ads")
    nguondoitac = fields.Many2one(
        'res.partner', string='Đối tác cung cấp',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        change_default=True)
    lifecyclemql = fields.Char(string="Life Cycle Stage")
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
    quocgiabook = fields.Selection([('uc', 'Úc'),
                                ('canada', 'Canada'),
                                ('ireland', 'Ireland')], 
                                string="Quốc gia Book", default=False)

    noidungtele = fields.Text(string="Nội dung cuộc gọi Telesales")
    hocvan = fields.Selection([('tieuhoc', 'Tiểu học'),
                                ('thcs', 'THCS'),
                                ('thpt', 'THPT'),
                                ('trungcap', 'Trung cấp'),
                                ('caodang', 'Cao đẳng'),
                                ('daihoc', 'Đại học')], 
                                string="Học vấn", default=False)
    trinhdotienganh = fields.Selection([('khong', 'Không'),
                                ('coban', 'Cơ bản'),
                                ('giaotiep', 'Giao tiếp'),
                                ('ie34pte23', 'Ielts 3.0-4.0/ PTE 23+'),
                                ('ie45pte29', 'Ielts 4.0-5.0 /PTE 29+'),
                                ('ie56pte36', 'Ielts 5.0-6.0 / PTE 36+'),
                                ('ie6pte46', 'Ielts trên 6.0 / PTE 46+')], 
                                string="Trình độ tiếng anh", default=False)
    color_data = fields.Selection([('xanh', 'Xanh'),
                                ('vang', 'Vàng'),
                                ('do', 'Đỏ')], 
                                string="Màu trạng thái", readonly=True, default=False)
    loai_data = fields.Selection([('mo', 'Mở')],
                                string="Loại data", readonly=True, default=False)                        
    ads_id = fields.Char(string="Ads ID")
    gioitinh = fields.Selection([
                                ('nam', 'Nam'),
                                ('nu', 'Nữ')       
                                ], string='Giới tính')


    def write(self, vals):
        # Kiểm tra xem có sửa hơn 20 bản ghi không
        if len(self) > 80:
            raise UserError("Bạn không thể sửa quá 80 bản ghi cùng lúc.")
        return super(bissweb, self).write(vals)


    def unlink(self):
        # Kiểm tra xem có xóa hơn 1 bản ghi không
        if len(self) > 10:
            raise UserError("Bạn không thể xóa nhiều bản ghi cùng lúc.")
        return super(bissweb, self).unlink()


    @api.model
    def _status_data_crm_scheduler(self):
        def process_leads(datetime_data, status=None, status_list=None):
            limit = 1000  # Number of records per page
            offset = 0
            while True:
                # Construct the search domain
                domain = [
                    ('type', '=', 'lead'),
                    ('write_date', '>=', datetime_data)
                ]
                if status:
                    domain.append(('trangthaidt', '=', status))
                elif status_list:
                    filtered_states = [state for state in status_list if state is not False]
                    domain.append(('trangthaidt', 'in', filtered_states))
                
                try:
                    # Paginated search for leads
                    leads = self.env['crm.lead'].sudo().search(domain, limit=limit, offset=offset)
                    
                    # If no leads are found, break the loop
                    if not leads:
                        break
                    
                    # Process each lead
                    for lead in leads:
                        lead.message_unsubscribe(partner_ids=lead.message_partner_ids.ids)
                        lead.write({
                            'user_id': False,
                            'team_id': False,
                            'loai_data': 'mo',
                            'color_data': False,
                        })
                    
                    # Log the number of leads processed
                    _logger.info(f"Processed {len(leads)} leads for datetime: {datetime_data}")
                    
                except Exception as e:
                    # Log the error if something goes wrong
                    _logger.error(f"Error processing leads for datetime {datetime_data}: {e}")
                
                # Move to the next page
                offset += limit

        # Define status lists
        status_list_1 = [
            'doituongchamsoc', 'doituongdungchamsoc', 'khongbatmay', 'khongbatmayhai', 'khongbatmayba',
            'khongbatmaybon', 'khongbatmaynam', 'khongconhucau', 'trungdata', 'saiso', 'daguitinzalokb',
            'khongdutaichinh', 'doituongdotuoilon'
        ]
        status_list = ['followdaihan', 'guiemailofferkh', 'guiemailhd', 'thamgiadgenglish', 'tiemnangkyhd']

        # Process leads based on different datetime and status filters
        datetime_data = fields.Datetime.today() + timedelta(days=1)
        process_leads(datetime_data, status=None, status_list=status_list_1)

        datetime_pitc = fields.Datetime.today() + timedelta(days=2)
        process_leads(datetime_pitc, status='bopitching')

        datetime_dungcs = fields.Datetime.today() + timedelta(days=3)
        process_leads(datetime_dungcs, status='doituongdungchamsoc')

        datetime_foll = fields.Datetime.today() + timedelta(days=7)
        process_leads(datetime_foll, status=None, status_list=status_list_1)

        datetime_daihans = fields.Datetime.today() + timedelta(days=14)
        process_leads(datetime_daihans, status=None, status_list=status_list)

        datetime_ngans = fields.Datetime.today() + timedelta(days=28)
        process_leads(datetime_ngans, status='follownganhan')


    #Hàm set màu
    @api.model
    def update_color_all_leads(self):
        def update_leads_color_data(target_date, state=None, list_states=None):
            """
            Cập nhật trường 'color_data' cho các bản ghi lead dựa trên ngày mục tiêu và trạng thái theo dõi.
            Sử dụng phân trang để xử lý tập dữ liệu lớn.

            :param target_date: Ngày mục tiêu để tính phạm vi ngày.
            :param state: Trạng thái theo dõi cho việc lọc lead (tùy chọn).
            :param list_states: Danh sách các trạng thái để lọc lead (tùy chọn). Nếu None, sử dụng trạng thái đơn.
            """
            try:
                # Tính toán các mốc thời gian
                datetime_min = target_date - timedelta(days=5)
                datetime_max = target_date - timedelta(days=3)
                datetime_range_2_start = target_date - timedelta(days=3)
                datetime_range_2_end = target_date
                datetime_range_3_start = target_date
                datetime_range_3_end = target_date + timedelta(days=3)

                # Khởi tạo phân trang
                page_size = 100
                page = 0

                # Xây dựng điều kiện tìm kiếm (domain)
                domain = [
                    ('type', '=', 'lead'),
                    ('write_date', '>=', datetime_min),
                    ('write_date', '<=', datetime_max),
                ]
                
                # Xử lý trạng thái
                if list_states:
                    # Lọc bỏ giá trị False trong list_states trước khi sử dụng
                    filtered_states = [state for state in list_states if state is not False]
                    if filtered_states:
                        domain.append(('trangthaidt', 'in', filtered_states))
                elif state:
                    domain.append(('trangthaidt', '=', state))  # Lọc theo một trạng thái duy nhất

                # Lặp qua phân trang
                while True:
                    leads = self.env['crm.lead'].sudo().search(domain, limit=page_size, offset=page * page_size)

                    if not leads:
                        break

                    leads_to_update = []

                    for lead in leads:
                        if datetime_min <= lead.write_date <= datetime_max:
                            leads_to_update.append((lead.id, 'xanh'))
                        elif datetime_range_2_start <= lead.write_date <= datetime_range_2_end:
                            leads_to_update.append((lead.id, 'vang'))
                        elif datetime_range_3_start <= lead.write_date <= datetime_range_3_end:
                            leads_to_update.append((lead.id, 'do'))

                    if leads_to_update:
                        leads_to_update_data = [{'id': lead_id, 'color_data': color} for lead_id, color in leads_to_update]
                        self.env['crm.lead'].sudo().write(leads_to_update_data)

                    page += 1
            except Exception as e:
                # Log error or handle exception appropriately
                print(f"Error updating leads color data: {str(e)}")

        # Set target dates and states
        datetime_foll = fields.Datetime.today() + timedelta(days=7)
        datetime_ngans = fields.Datetime.today() + timedelta(days=28)
        datetime_daihan = fields.Datetime.today() + timedelta(days=14)
        list_states_daihan = [False, 'followdaihan', 'guiemailofferkh', 'guiemailhd', 'thamgiadgenglish', 'tiemnangkyhd']
        list_states_foll = [False, 'khongbatmay','khongbatmayhai','khongbatmayba','khongbatmaybon','khongbatmaynam','khongconhucau','trungdata','saiso','daguitinzalokb','khongdutaichinh','doituongdotuoilon']

        # Update leads color for different target dates and states
        update_leads_color_data(datetime_ngans, state='follownganhan')  # Trạng thái đơn
        update_leads_color_data(datetime_daihan, list_states=list_states_daihan)  # Nhiều trạng thái
        update_leads_color_data(datetime_foll, list_states=list_states_foll)  # Nhiều trạng thái



    def action_sync_mql(self):
        for rec in self:
            rec.onchange_trangthaidt()  

    # Trang thai IQL
    @api.onchange('trangthaidt')
    def onchange_trangthaidt(self):
        self.lifecyclemql = 'IQL'
         #MQL
        if self.trangthaidt == '':
            self.lifecyclemql = 'IQL'
        elif self.trangthaidt == 'khongbatmay':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khongbatmayhai':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khongbatmayba':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khongbatmaybon':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khongbatmaynam':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khongconhucau':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'hengoilai':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'trungdata':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'saiso':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'daguitinzalokb':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'lylichtpxau':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khongdutaichinh':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'doituongdotuoilon':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'quantambhpxkld':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'taichinhchuadu':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'timhieuthem':
            self.lifecyclemql = 'MQL'
        elif self.trangthaidt == 'khac':
            self.lifecyclemql = 'MQL'
        #SQL
        elif self.trangthaidt == 'bopitching':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'thamgiapitching':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'doituongchamsoc':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'doituongdungchamsoc':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'follownganhan':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'followdaihan':
            self.lifecyclemql = 'SQL'  
        elif self.trangthaidt == 'pitchingguithamdinh':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'thamgiareview':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'tiemnangkyhd':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'guiemailofferkh':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'guiemailhd':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'thamgiadgenglish':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'deposit':
            self.lifecyclemql = 'SQL'
        elif self.trangthaidt == 'doituongkhongphuhop':
            self.lifecyclemql = 'SQL'            
        #Customer
        elif self.trangthaidt == 'dakyhdttmot':
            self.lifecyclemql = 'Customer'
        elif self.trangthaidt == 'daxeplopta':
            self.lifecyclemql = 'Customer'
        elif self.trangthaidt == 'daxeplopdtn':
            self.lifecyclemql = 'Customer'
        elif self.trangthaidt == 'daotaopv':
            self.lifecyclemql = 'Customer'
        elif self.trangthaidt == 'ttlanhai':
            self.lifecyclemql = 'Customer'

class ResPartner(models.Model):
    _inherit = 'res.partner'

    same_mobile_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_same_mobile_partner_id",
        string="Partner with same mobile",
        compute_sudo=True,
    )

    @api.depends("mobile", "company_id")
    def _compute_same_mobile_partner_id(self):
        # With phone_validation, the "mobile" field should be
        # clean in E.164 format, without any start/ending spaces
        # So we search on the 'mobile' field with '=' !
        for partner in self:
            same_mobile_partner_id = False
            if partner.mobile:
                domain = [("mobile", "=", partner.mobile)]
                if partner.company_id:
                    domain += [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                partner_id = partner._origin.id
                if partner_id:
                    domain.append(("id", "!=", partner_id))
                same_mobile_partner = self.with_context(active_test=False).search(
                    domain, limit=1
                )
                same_mobile_partner_id = same_mobile_partner.id or False
            partner.same_mobile_partner_id = same_mobile_partner_id


    same_email_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_same_email_partner_id",
        string="Partner with same e-mail",
        compute_sudo=True,
    )

    @api.depends("email", "company_id")
    def _compute_same_email_partner_id(self):
        for partner in self:
            same_email_partner_id = False
            if partner.email and partner.email.strip():
                partner_email = partner.email.strip().lower()
                domain = [("email", "=ilike", "%" + partner_email + "%")]
                if partner.company_id:
                    domain += [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                partner_id = partner._origin.id
                if partner_id:
                    domain += [
                        ("id", "!=", partner_id),
                        "!",
                        ("id", "child_of", partner_id),
                        "!",
                        ("id", "parent_of", partner_id),
                    ]
                search_partners = self.with_context(active_test=False).search(domain)
                for search_partner in search_partners:
                    if (
                        search_partner.email
                        and search_partner.email.strip().lower() == partner_email
                    ):
                        same_email_partner_id = search_partner
                        break
            partner.same_email_partner_id = same_email_partner_id


class Employeemore(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

              
    namsinhnv = fields.Date(string="Năm sinh", groups="hr.group_hr_user")
    dcccdnv = fields.Char(string="CCCD", groups="hr.group_hr_user")
    diachinv = fields.Text(string="Địa chỉ", groups="hr.group_hr_user")
    masothue = fields.Char(string="Mã số thuế", groups="hr.group_hr_user")
    hopdongnv = fields.Char(string="Hợp đồng", groups="hr.group_hr_user")
    loaihdnv = fields.Selection([('chinhthuc', 'Chính thức'), ('thuviec', 'Thử việc'), ('khoanviec', 'Khoán việc'), ('ctv', 'CTV')],
        string="Loại hợp đồng", groups="hr.group_hr_user")
    mucluongcb = fields.Monetary(string='Mức lương',currency_field='currency_id', groups="hr.group_hr_user")
    currency_id = fields.Many2one('res.currency', string="Đơn vị tiền", store=True, readonly=False, groups="hr.group_hr_user")   
    ngaykyhd = fields.Date(string='Ngày ký HĐ', groups="hr.group_hr_user")
    ngaykthd = fields.Date(string='Ngày Kết thúc HĐ', groups="hr.group_hr_user")
    gioitinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ')
    ], string='Giới tính', groups="hr.group_hr_user")

#     hopdongns_ids = fields.One2many('comodel_name', 'inverse_field_name', string='field_name')


# class Employeemore(models.Model):
#     _name = 'hr.employee'
#     _inherit = 'hr.employee'



 
