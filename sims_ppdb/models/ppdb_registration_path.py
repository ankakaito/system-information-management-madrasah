from odoo import fields, models, api, _


class SimsPpdbRegistrationPath(models.Model):
    _name = 'sims.ppdb.registration.path'
    _description = 'Master Jalur Pendaftaran PPDB'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nama Jalur',
        required=True,
    )

    code = fields.Char(
        string='Kode Jalur',
        readonly=True,
        copy=False,
    )

    description = fields.Text(
        string='Deskripsi',
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
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
                        'sims.ppdb.registration.path'
                    ) or 'New'
                )
        return super().create(vals_list)

    _sql_constraints = [
        (
            'code_unique',
            'unique(code)',
            'Kode jalur pendaftaran harus unik.',
        ),
        (
            'name_unique',
            'unique(name)',
            'Nama jalur pendaftaran harus unik.',
        ),
    ]
