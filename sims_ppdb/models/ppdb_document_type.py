from odoo import fields, models, api


class SimsPpdbDocumentType(models.Model):
    _name = 'sims.ppdb.document.type'
    _description = 'Master Jenis Dokumen PPDB'
    _order = 'code'

    name = fields.Char(
        string='Nama Dokumen',
        required=True,
    )

    code = fields.Char(
        string='Kode Dokumen',
        readonly=True,
        copy=False,
    )

    description = fields.Text(
        string='Keterangan',
    )

    is_required_default = fields.Boolean(
        string='Wajib Secara Default',
        default=True,
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
                        'sims.ppdb.document.type'
                    ) or 'New'
                )
        return super().create(vals_list)

    _sql_constraints = [
        (
            'code_unique',
            'unique(code)',
            'Kode dokumen harus unik.'
        ),
        (
            'name_unique',
            'unique(name)',
            'Nama dokumen harus unik.'
        ),
    ]

