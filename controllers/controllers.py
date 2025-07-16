import werkzeug
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.osv import expression
from werkzeug.utils import secure_filename
from odoo.exceptions import ValidationError
import os
import base64
from datetime import datetime


class Bissweb(http.Controller):

    @http.route('/form_custumer/<int:lead_id>', type='http', auth='public', csrf=False,website=True)
    def form_custumer(self, lead_id, **kwargs):
        # Render the form template
        # return request.render('bissweb.form_templates', {
        #     'name': name,
        #     'phone': phone,
        #     'email': email
        # })


        lead = request.env['formreview.lead'].sudo().browse(lead_id)
        if not lead.exists():
            return request.not_found()
        if lead.close_form:
                 return request.render('bissweb.custom_form_no_lead')
        
        return request.render('bissweb.form_templates', {
            'lead': lead,
        })

    # Route mới - Form công khai độc lập
    @http.route('/form_custumer', type='http', auth='public', csrf=False, website=True)
    def form_customer_public(self, **kwargs):
        """Form công khai không cần lead_id"""
        return request.render('bissweb.form_templates_public', {
            'is_public': True,
        })
    
    #Submit cũ - Form theo ID
    @http.route('/submit_lead_form', type='http', auth='public',website=True,csrf=False, methods=['POST'])
    def submit_lead_form(self, **kwargs):
        lead_id = int(kwargs.get('lead_id'))
        lead = request.env['formreview.lead'].sudo().browse(lead_id)
        if lead.close_form:
            return request.render('bissweb.custom_form_no_lead')
        if lead.exists():
            lead.write({
                'quoctich': kwargs.get('quoctich'),
                'gioitinh': kwargs.get('gioitinh'),
                'namsinhnd': kwargs.get('namsinhnd'),
                'email': kwargs.get('email'),
                'phone': kwargs.get('phone'),
                'hkthuongtru': kwargs.get('hkthuongtru'),
                'noio': kwargs.get('noio'),
                'tinhtranghn': kwargs.get('tinhtranghn'),
                'nguyenvongdd': kwargs.get('nguyenvongdd'),
                'nhucau': kwargs.get('nhucau'),
                'visa': kwargs.get('visa'),
                'quocgiabook': kwargs.get('quocgiabook'),
                'nghebooking': kwargs.get('nghebooking'),
                'nguoithan': kwargs.get('nguoithan'),
                'chungchitaynghe': kwargs.get('chungchitaynghe'),
                'bangcap': kwargs.get('bangcap'),
                'chuyennganh': kwargs.get('chuyennganh'),
                #'truongcap': kwargs.get('truongcap'),
                'namtotnghiep': kwargs.get('namtotnghiep'),
                'tienganh': kwargs.get('tienganh'),
                'chungchita': kwargs.get('chungchita'),
                'namcapccta': kwargs.get('namcapccta'),
                'congviecht': kwargs.get('congviecht'),
                'tendoanhnghiepht': kwargs.get('tendoanhnghiepht'),
                'thoigianlamht': kwargs.get('thoigianlamht'),
                'kinhnghiemht':kwargs.get('kinhnghiemht'),
                'congviectruocday':kwargs.get('congviectruocday'),
                'tendoanhnghiep' : kwargs.get('tendoanhnghiep'),
                'thoigianlam' : kwargs.get('thoigianlam'),
                'kinhnghiem' : kwargs.get('kinhnghiem'),
                'capvisadulichvfs' : kwargs.get('capvisadulichvfs'),
                'capvisalaodongvfs' : kwargs.get('capvisalaodongvfs'),
                'capvisaqgkhac' : kwargs.get('capvisaqgkhac'),
                #'caplaivisa' : kwargs.get('caplaivisa'),
                #'tuchoivisagd' : kwargs.get('tuchoivisagd'),
                'phamphap' : kwargs.get('phamphap'),
                'suckhoe' : kwargs.get('suckhoe'),
                #'nguoitaitro_dh' : kwargs.get('nguoitaitro_dh'),
                #'luongthangdd_dh' : kwargs.get('luongthangdd_dh'),
                #'luongthangpt_dh' : kwargs.get('luongthangpt_dh'),
                #'thunhapbds_dh' : kwargs.get('thunhapbds_dh'),
                'sotk_dh' : kwargs.get('sotk_dh'),
                'tsbds_dh' : kwargs.get('tsbds_dh'),
                #'luongthang' : kwargs.get('luongthang'),
                #'luongthang_pt' : kwargs.get('luongthang_pt'),
                #'thunhapbds' : kwargs.get('thunhapbds'),
                'sotk' : kwargs.get('sotk'),
                'tsbds' : kwargs.get('tsbds'),
                'hinhthucdn' : kwargs.get('hinhthucdn'),
                'dongthuedn' : kwargs.get('dongthuedn'),
                'giayphepkddn' : kwargs.get('giayphepkddn'),
                'mst_webdn' : kwargs.get('mst_webdn'),
                'thunhapbdsdn' : kwargs.get('thunhapbdsdn'),
                'sotkdn' : kwargs.get('sotkdn'),
                'bdsdn' : kwargs.get('bdsdn'),
                'name_npt' : kwargs.get('name_npt'),
                'namsinh_npt' : kwargs.get('namsinh_npt'),
                'bangcap_npt' : kwargs.get('bangcap_npt'),
                'cvht_npt' : kwargs.get('cvht_npt'),
                'tienganh_npt' : kwargs.get('tienganh_npt'),
                'close_form' : kwargs.get('close_form'),
            })
            

            # Process file if uploaded
            file = request.httprequest.files.get('file', None)
            attachment = None
            if file:
                # Check that the file is a werkzeug FileStorage object (which should have filename attribute)
                if isinstance(file, werkzeug.datastructures.FileStorage):
                    # Secure the filename and check the file type and size
                    file_name = secure_filename(file.filename)
                    file_size = len(file.read())  # Measure file size

                    if file_size > 5 * 1024 * 1024:  # 5MB max size
                        return request.render('bissweb.error_template', {'error_message': 'File size exceeds 5MB!'})

                    # Rewind the file after checking size
                    file.seek(0)
                    
                    # Save the file as an attachment in Odoo (base64 encode)
                    file_content = base64.b64encode(file.read())
                    attachment_data = {
                        'name': file_name,
                        'datas': file_content,
                        'type': 'binary',
                        'mimetype': file.content_type,
                        'res_model': 'formreview.lead',
                        'res_id': lead.id,
                        'public': True,
                    }
                    attachment = request.env['ir.attachment'].sudo().create(attachment_data)
                else:
                    return request.render('bissweb.error_template', {'error_message': 'Uploaded file is not valid.'})

            # If file was uploaded, link it to the lead
            if attachment:
                attachment.write({'res_model': 'formreview.lead', 'res_id': lead.id})

            return request.render('bissweb.custom_form_thankyou_template')
    # Submit mới - Form công khai độc lập
    @http.route('/submit_public_form', type='http', auth='public', website=True, csrf=False, methods=['POST'])
    def submit_public_form(self, **kwargs):
        try:
            # Kiểm tra thông tin bắt buộc
            if not kwargs.get('name') or not kwargs.get('email') or not kwargs.get('phone'):
                return request.render('bissweb.error_template', {
                    'error_message': 'Vui lòng điền đầy đủ thông tin bắt buộc: Họ tên, Email và Số điện thoại'
                })

            # 1. Tạo CRM Lead (crm.lead)
            crm_lead = request.env['crm.lead'].sudo().create({
                'name': kwargs.get('name'),
                'email_from': kwargs.get('email'),
                'phone': kwargs.get('phone'),
            })

            # 2. Tạo bản ghi formreview.lead và liên kết lead_form_id
            form_data = {
                'lead_form_id': crm_lead.id,
                'quoctich': kwargs.get('quoctich'),
                'gioitinh': kwargs.get('gioitinh'),
                'namsinhnd': kwargs.get('namsinhnd'),
                'email': kwargs.get('email'),
                'phone': kwargs.get('phone'),
                'hkthuongtru': kwargs.get('hkthuongtru'),
                'noio': kwargs.get('noio'),
                'tinhtranghn': kwargs.get('tinhtranghn'),
                'nguyenvongdd': kwargs.get('nguyenvongdd'),
                'nhucau': kwargs.get('nhucau'),
                'visa': kwargs.get('visa'),
                'quocgiabook': kwargs.get('quocgiabook'),
                'nghebooking': kwargs.get('nghebooking'),
                'nguoithan': kwargs.get('nguoithan'),
                'chungchitaynghe': kwargs.get('chungchitaynghe'),
                'bangcap': kwargs.get('bangcap'),
                'chuyennganh': kwargs.get('chuyennganh'),
                #'truongcap': kwargs.get('truongcap'),
                'namtotnghiep': kwargs.get('namtotnghiep'),
                'tienganh': kwargs.get('tienganh'),
                'chungchita': kwargs.get('chungchita'),
                'namcapccta': kwargs.get('namcapccta'),
                'congviecht': kwargs.get('congviecht'),
                'tendoanhnghiepht': kwargs.get('tendoanhnghiepht'),
                'thoigianlamht': kwargs.get('thoigianlamht'),
                'kinhnghiemht': kwargs.get('kinhnghiemht'),
                'congviectruocday': kwargs.get('congviectruocday'),
                'tendoanhnghiep': kwargs.get('tendoanhnghiep'),
                'thoigianlam': kwargs.get('thoigianlam'),
                'kinhnghiem': kwargs.get('kinhnghiem'),
                'capvisadulichvfs': kwargs.get('capvisadulichvfs'),
                'capvisalaodongvfs': kwargs.get('capvisalaodongvfs'),
                'capvisaqgkhac': kwargs.get('capvisaqgkhac'),
                #'caplaivisa': kwargs.get('caplaivisa'),
                #'tuchoivisagd': kwargs.get('tuchoivisagd'),
                'phamphap': kwargs.get('phamphap'),
                'suckhoe': kwargs.get('suckhoe'),
                #'nguoitaitro_dh': kwargs.get('nguoitaitro_dh'),
                #'luongthangdd_dh': kwargs.get('luongthangdd_dh'),
                #'luongthangpt_dh': kwargs.get('luongthangpt_dh'),
                #'thunhapbds_dh': kwargs.get('thunhapbds_dh'),
                'sotk_dh': kwargs.get('sotk_dh'),
                'tsbds_dh': kwargs.get('tsbds_dh'),
                'luongthang': kwargs.get('luongthang'),
                'luongthang_pt': kwargs.get('luongthang_pt'),
                'thunhapbds': kwargs.get('thunhapbds'),
                'sotk': kwargs.get('sotk'),
                'tsbds': kwargs.get('tsbds'),
                'hinhthucdn': kwargs.get('hinhthucdn'),
                'dongthuedn': kwargs.get('dongthuedn'),
                'giayphepkddn': kwargs.get('giayphepkddn'),
                'mst_webdn': kwargs.get('mst_webdn'),
                'thunhapbdsdn': kwargs.get('thunhapbdsdn'),
                'sotkdn': kwargs.get('sotkdn'),
                'bdsdn': kwargs.get('bdsdn'),
                'name_npt': kwargs.get('name_npt'),
                'namsinh_npt': kwargs.get('namsinh_npt'),
                'bangcap_npt': kwargs.get('bangcap_npt'),
                'cvht_npt': kwargs.get('cvht_npt'),
                'tienganh_npt': kwargs.get('tienganh_npt'),
                'is_public_form': True,
                'close_form': True,
            }

            form_lead = request.env['formreview.lead'].sudo().create(form_data)

            # 3. Xử lý file upload (nếu có)
            file = request.httprequest.files.get('file', None)
            if file and isinstance(file, werkzeug.datastructures.FileStorage):
                file_name = secure_filename(file.filename)
                file_size = len(file.read())
                if file_size > 5 * 1024 * 1024:
                    return request.render('bissweb.error_template', {
                        'error_message': 'Kích thước file vượt quá 5MB!'
                    })
                file.seek(0)
                file_content = base64.b64encode(file.read())
                request.env['ir.attachment'].sudo().create({
                    'name': file_name,
                    'datas': file_content,
                    'type': 'binary',
                    'mimetype': file.content_type,
                    'res_model': 'formreview.lead',
                    'res_id': form_lead.id,
                    'public': True,
                })
            # 🆕 4. GỬI EMAIL THÔNG BÁO ĐẾN ADMIN - PHẦN MỚI BẮT ĐẦU TỪ ĐÂY
            try:
                # Tạo nội dung email
                current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                email_body = f"""
                <h2>🔔 Thông báo: Khách hàng mới điền form công khai</h2>
                
                <h3>📋 Thông tin cơ bản:</h3>
                <ul>
                    <li><strong>Họ và tên:</strong> {kwargs.get('name', 'Không có')}</li>
                    <li><strong>Email:</strong> {kwargs.get('email', 'Không có')}</li>
                    <li><strong>Số điện thoại:</strong> {kwargs.get('phone', 'Không có')}</li>
                    <li><strong>Thời gian gửi:</strong> {current_time}</li>
                </ul>
                
                <h3>🎯 Nguyện vọng:</h3>
                <ul>
                    <li><strong>Loại visa:</strong> {dict(form_lead._fields['visa'].selection).get(kwargs.get('visa', ''), 'Không chọn')}</li>
                    <li><strong>Quốc gia:</strong> {dict(form_lead._fields['quocgiabook'].selection).get(kwargs.get('quocgiabook', ''), 'Không chọn')}</li>
                    <li><strong>Nghề nghiệp:</strong> {dict(form_lead._fields['nghebooking'].selection).get(kwargs.get('nghebooking', ''), 'Không chọn')}</li>
                    <li><strong>Nhu cầu:</strong> {kwargs.get('nhucau', 'Không có')}</li>
                </ul>
                
                <h3>🎓 Trình độ:</h3>
                <ul>
                    <li><strong>Bằng cấp:</strong> {dict(form_lead._fields['bangcap'].selection).get(kwargs.get('bangcap', ''), 'Không chọn')}</li>
                    <li><strong>Tiếng Anh:</strong> {dict(form_lead._fields['tienganh'].selection).get(kwargs.get('tienganh', ''), 'Không chọn')}</li>
                    <li><strong>Chuyên ngành:</strong> {kwargs.get('chuyennganh', 'Không có')}</li>
                </ul>
                
                <h3>🔗 Liên kết:</h3>
                <p><a href="{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/web#id={form_lead.id}&view_type=form&model=formreview.lead" 
                    style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                📂 Xem chi tiết trong hệ thống</a></p>
                
                <hr/>
                <p><em>Email này được gửi tự động từ hệ thống DSS Education.</em></p>
                """
                
                # Gửi email
                mail_values = {
                    'subject': f'🔔 Khách hàng mới: {kwargs.get("name", "Không rõ tên")} - Form công khai',
                    'body_html': email_body,
                    'email_to': 'thienhm@dsseducationgroup.com',
                    'email_from': request.env.user.email or 'noreply@dsseducation.com',
                    'auto_delete': False,
                    'model': 'formreview.lead',
                    'res_id': form_lead.id,
                }
                
                mail = request.env['mail.mail'].sudo().create(mail_values)
                mail.send()
                
            except Exception as email_error:
                # Log lỗi email nhưng không làm gián đoạn quá trình
                request.env.cr.rollback()
                import logging
                _logger = logging.getLogger(__name__)
                _logger.error(f"Lỗi gửi email thông báo: {str(email_error)}")
            return request.render('bissweb.custom_form_thankyou_template')

        except Exception as e:
            return request.render('bissweb.error_template', {
                'error_message': f'Có lỗi xảy ra khi xử lý form: {str(e)}'
            })
