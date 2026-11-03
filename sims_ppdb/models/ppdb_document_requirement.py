from odoo import fields, models


class SimsPpdbDocumentRequirement(models.Model):
    _name = 'sims.ppdb.document.requirement'
    _description = 'Persyaratan Dokumen PPDB'
    _order = 'sequence, id'

    wave_path_id = fields.Many2one(
        comodel_name='sims.ppdb.wave.path',
        string='Jalur Pendaftaran per Gelombang',
        required=True,
        ondelete='cascade',
    )

    document_type_id = fields.Many2one(
        comodel_name='sims.ppdb.document.type',
        string='Jenis Dokumen',
        required=True,
        ondelete='restrict',
    )

    is_required = fields.Boolean(
        string='Wajib',
        default=True,
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
            'wave_path_document_type_unique',
            'unique(wave_path_id, document_type_id)',
            'Jenis dokumen tersebut sudah ditambahkan pada jalur ini.',
        ),
    ]
