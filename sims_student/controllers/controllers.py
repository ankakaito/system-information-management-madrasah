# from odoo import http


# class SimsStudent(http.Controller):
#     @http.route('/sims_student/sims_student', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sims_student/sims_student/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sims_student.listing', {
#             'root': '/sims_student/sims_student',
#             'objects': http.request.env['sims_student.sims_student'].search([]),
#         })

#     @http.route('/sims_student/sims_student/objects/<model("sims_student.sims_student"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sims_student.object', {
#             'object': obj
#         })

