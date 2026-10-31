
from odoo import models, fields, api, _


class PpdbAchievementType(models.Model):
    _name = 'sims.ppdb.achievement.type'
    _description = 'Master Jenis Prestasi PPDB'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nama Prestasi',
        required=True,
    )

    code = fields.Char(
        string='Kode Prestasi',
        readonly=True,
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


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals.get('code') == 'New':
                vals['code'] = (
                    self.env['ir.sequence'].next_by_code(
                        'sims.ppdb.achievement.type'
                    ) or 'New'
                )
        return super().create(vals_list)
    
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

