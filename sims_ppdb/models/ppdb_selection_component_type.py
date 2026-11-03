from odoo import fields, models


class SimsPpdbSelectionComponentType(models.Model):
    _name = 'sims.ppdb.selection.component.type'
    _description = 'Jenis Komponen Seleksi'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nama Jenis Komponen',
        required=True,
    )

    code = fields.Char(
        string='Kode',
        required=True,
    )

    description = fields.Text(
        string='Keterangan',
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
            'Kode jenis komponen sudah digunakan.',
        ),
        (
            'name_unique',
            'unique(name)',
            'Nama jenis komponen sudah digunakan.',
        ),
    ]
