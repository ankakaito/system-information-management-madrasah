
from odoo import models, fields


class PpdbAchievementType(models.Model):
    _name = 'sims.ppdb.achievement.type'
    _description = 'Master Jenis Prestasi PPDB'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nama Prestasi',
        required=True,
    )

    code = fields.Char(
        string='Kode',
        required=True,
        copy=False,
    )

    category = fields.Selection(
        selection=[
            ('academic', 'Akademik'),
            ('sports', 'Olahraga'),
            ('arts', 'Seni'),
            ('religious', 'Keagamaan'),
            ('other', 'Lainnya'),
        ],
        string='Kategori',
        required=True,
        default='other',
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
            'achievement_type_code_unique',
            'unique(code)',
            'Kode jenis prestasi harus unik.',
        ),
        (
            'achievement_type_name_unique',
            'unique(name)',
            'Nama jenis prestasi harus unik.',
        ),
    ]

