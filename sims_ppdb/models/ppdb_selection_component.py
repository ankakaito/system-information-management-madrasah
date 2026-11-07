from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SimsPpdbSelectionComponent(models.Model):
    _name = 'sims.ppdb.selection.component'
    _description = 'Master Komponen Seleksi PPDB'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nama Komponen',
        required=True,
    )

    code = fields.Char(
        string='Kode Komponen',
        readonly=True,
        copy=False,
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
    )

    description = fields.Text(
        string='Keterangan',
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals.get('code') == 'New':
                vals['code'] = (
                    self.env['ir.sequence'].next_by_code(
                        'sims.ppdb.selection.component'
                    ) or 'New'
                )
        return super().create(vals_list)

    _sql_constraints = [
        (
            'code_unique',
            'unique(code)',
            'Kode komponen harus unik.'
        ),
        (
            'name_unique',
            'unique(name)',
            'Nama komponen harus unik.'
        ),
    ]

    def _check_values(self):
        for record in self:
            if record.max_score <= 0:
                raise ValidationError(
                    _('Nilai maksimal harus lebih dari nol.')
                )
            if record.weight < 0 or record.weight > 100:
                raise ValidationError(
                    _('Bobot harus berada pada rentang 0 sampai 100.')
                )

