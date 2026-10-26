
from odoo import fields, models, _
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
        required=True,
    )

    component_type = fields.Selection(
        [
            ('academic', 'Akademik'),
            ('quran', "Baca Al-Qur'an"),
            ('interview', 'Wawancara'),
            ('other', 'Lainnya'),
        ],
        string='Jenis Komponen',
        required=True,
        default='academic',
    )

    max_score = fields.Float(
        string='Nilai Maksimal',
        required=True,
        default=100.0,
    )

    weight = fields.Float(
        string='Bobot (%)',
        required=True,
        default=0.0,
    )

    is_required = fields.Boolean(
        string='Wajib Diikuti',
        default=True,
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
        (
            'max_score_positive',
            'check(max_score > 0)',
            'Nilai maksimal harus lebih dari nol.'
        ),
        (
            'weight_range',
            'check(weight >= 0 and weight <= 100)',
            'Bobot harus berada pada rentang 0 sampai 100.'
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

