from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SimsPpdbWavePathSelectionLine(models.Model):
    _name = 'sims.ppdb.wave.path.selection.line'
    _description = 'Detail Komponen Seleksi per Jalur'
    _order = 'selection_config_id, sequence, id'

    selection_config_id = fields.Many2one(
        comodel_name='sims.ppdb.wave.path.selection',
        string='Konfigurasi Seleksi',
        required=True,
        ondelete='cascade',
    )

    selection_component_id = fields.Many2one(
        comodel_name='sims.ppdb.selection.component',
        string='Komponen Seleksi',
        required=True,
        ondelete='restrict',
        domain="[('active', '=', True)]",
    )

    max_score = fields.Float(
        string='Nilai Maksimal',
        required=True,
        default=100.0,
    )

    min_score = fields.Float(
        string='Nilai Ambang Batas',
        required=True,
        default=0.0,
    )

    weight = fields.Float(
        string='Bobot (%)',
        required=True,
        default=0.0,
    )

    is_required = fields.Boolean(
        string='Wajib',
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
            'selection_component_unique',
            'unique(selection_config_id, selection_component_id)',
            'Komponen seleksi tersebut sudah ditambahkan.',
        ),
    ]

    @api.constrains('max_score', 'min_score')
    def _check_score_range(self):
        for record in self:
            if record.max_score <= 0:
                raise ValidationError(
                    _('Nilai maksimal harus lebih besar dari 0.')
                )

            if record.min_score < 0:
                raise ValidationError(
                    _('Nilai ambang batas tidak boleh negatif.')
                )

            if record.min_score > record.max_score:
                raise ValidationError(
                    _('Nilai ambang batas tidak boleh melebihi nilai maksimal.')
                )

    @api.constrains('weight')
    def _check_weight(self):
        for record in self:
            if record.weight < 0 or record.weight > 100:
                raise ValidationError(
                    _('Bobot harus berada antara 0 sampai 100 persen.')
                )
