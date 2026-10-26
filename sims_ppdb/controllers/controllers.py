# from odoo import http


# class SimsPpdb(http.Controller):
#     @http.route('/sims_ppdb/sims_ppdb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sims_ppdb/sims_ppdb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sims_ppdb.listing', {
#             'root': '/sims_ppdb/sims_ppdb',
#             'objects': http.request.env['sims_ppdb.sims_ppdb'].search([]),
#         })

#     @http.route('/sims_ppdb/sims_ppdb/objects/<model("sims_ppdb.sims_ppdb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sims_ppdb.object', {
#             'object': obj
#         })

