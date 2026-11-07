
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class SimsPpdbWavePathSelection(models.Model):
    _name = 'sims.ppdb.wave.path.selection'
    _description = 'Konfigurasi Komponen Seleksi per Jalur'
    _order = 'wave_path_id, id'

    # =====================================================
    # INFORMASI KONFIGURASI
    # =====================================================

    name = fields.Char(
        string='Nama Konfigurasi',
        compute='_compute_name',
        store=True,
    )

    wave_path_id = fields.Many2one(
        comodel_name='sims.ppdb.wave.path',
        string='Jalur Pendaftaran per Gelombang',
        required=True,
        ondelete='cascade',
    )

    selection_component_ids = fields.One2many(
        comodel_name='sims.ppdb.wave.path.selection.line',
        inverse_name='selection_config_id',
        string='Komponen Seleksi',
    )

    description = fields.Text(
        string='Keterangan',
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
    )

    # =====================================================
    # TOTAL BOBOT
    # =====================================================

    total_weight = fields.Float(
        string='Total Bobot (%)',
        compute='_compute_total_weight',
        store=True,
        readonly=True,
        digits=(16, 2),
    )

    # =====================================================
    # COMPUTE NAMA KONFIGURASI
    # =====================================================

    @api.depends('wave_path_id.name')
    def _compute_name(self):
        for record in self:
            record.name = (
                record.wave_path_id.name
                if record.wave_path_id
                else 'New'
            )

    # =====================================================
    # COMPUTE TOTAL BOBOT
    # =====================================================

    @api.depends('selection_component_ids.weight')
    def _compute_total_weight(self):
        for record in self:
            record.total_weight = sum(
                record.selection_component_ids.mapped('weight')
            )

    # =====================================================
    # VALIDASI TOTAL BOBOT
    # =====================================================

    def _validate_total_weight(self):
        for record in self:
            total = sum(
                record.selection_component_ids.mapped('weight')
            )

            if float_compare(
                total,
                100.0,
                precision_digits=2
            ) > 0:
                raise ValidationError(
                    _('Bobot komponen seleksi tidak boleh lebih dari 100%.')
                )

    @api.constrains('selection_component_ids')
    def _check_total_weight(self):
        self._validate_total_weight()

    # =====================================================
    # SQL CONSTRAINT
    # =====================================================

    _wave_path_unique = models.Constraint(
        'UNIQUE(wave_path_id)',
        'Konfigurasi seleksi untuk jalur ini sudah tersedia.',
    )

