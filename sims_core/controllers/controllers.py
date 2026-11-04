# from odoo import http


# class SimsCore(http.Controller):
#     @http.route('/sims_core/sims_core', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sims_core/sims_core/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sims_core.listing', {
#             'root': '/sims_core/sims_core',
#             'objects': http.request.env['sims_core.sims_core'].search([]),
#         })

#     @http.route('/sims_core/sims_core/objects/<model("sims_core.sims_core"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sims_core.object', {
#             'object': obj
#         })

