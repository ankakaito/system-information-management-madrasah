from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsPpdbWavePathSelection(models.Model):
    _name = 'sims.ppdb.wave.path.selection'
    _description = 'Konfigurasi Komponen Seleksi per Jalur'
    _order = 'wave_path_id, id'

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

    @api.depends('wave_path_id.name')
    def _compute_name(self):
        for record in self:
            record.name = (
                record.wave_path_id.name
                if record.wave_path_id
                else 'New'
            )

    _sql_constraints = [
        (
            'wave_path_unique',
            'unique(wave_path_id)',
            'Konfigurasi seleksi untuk jalur ini sudah tersedia.',
        ),
    ]
