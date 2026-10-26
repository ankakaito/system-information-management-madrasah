from odoo import fields, models


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
        required=True,
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
