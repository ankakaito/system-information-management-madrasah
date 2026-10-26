from odoo import fields, models


class SimsPpdbDocumentType(models.Model):
    _name = 'sims.ppdb.document.type'
    _description = 'Master Jenis Dokumen PPDB'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nama Dokumen',
        required=True,
    )

    code = fields.Char(
        string='Kode Dokumen',
        required=True,
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

