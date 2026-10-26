# from odoo import models, fields, api


# class sims_student(models.Model):
#     _name = 'sims_student.sims_student'
#     _description = 'sims_student.sims_student'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

