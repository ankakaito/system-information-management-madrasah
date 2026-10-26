
from odoo import models, fields


class PpdbDocumentRequirement(models.Model):
    _name = 'sims.ppdb.document.requirement'
    _description = 'Persyaratan Dokumen PPDB'
    _order = 'period_id, sequence, id'

    period_id = fields.Many2one(
        comodel_name='sims.ppdb.period',
        string='Periode PPDB',
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
        string='Keterangan Persyaratan',
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
            'period_document_type_unique',
            'unique(period_id, document_type_id)',
            'Jenis dokumen hanya boleh ditambahkan satu kali dalam periode yang sama.',
        ),
    ]

