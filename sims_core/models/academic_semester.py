from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsAcademicSemester(models.Model):
    _name = 'sims.academic.semester'
    _description = 'Semester'
    _order = 'sequence, date_start, id'

    name = fields.Char(
        string='Nama Semester',
        required=True,
    )

    code = fields.Char(
        string='Kode Semester',
        required=True,
        copy=False,
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
    )

    academic_year_id = fields.Many2one(
        'sims.academic.year',
        string='Tahun Ajaran',
        required=True,
        ondelete='restrict',
        index=True,
    )

    date_start = fields.Date(
        string='Tanggal Mulai',
        required=True,
    )

    date_end = fields.Date(
        string='Tanggal Selesai',
        required=True,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Aktif'),
        ('closed', 'Ditutup'),
    ], string='Status', default='draft', required=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'semester_code_year_unique',
            'unique(academic_year_id, code)',
            'Kode semester harus unik dalam satu tahun ajaran.'
        ),
    ]

    @api.constrains(
        'date_start',
        'date_end',
        'academic_year_id'
    )
    def _check_dates(self):
        for record in self:
            if not record.academic_year_id:
                continue

            year = record.academic_year_id

            if record.date_start > record.date_end:
                raise ValidationError(
                    _('Tanggal mulai harus sebelum tanggal selesai.')
                )

            if (
                record.date_start < year.date_start
                or record.date_end > year.date_end
            ):
                raise ValidationError(
                    _('Tanggal semester harus berada '
                      'dalam periode tahun ajaran.')
                )

            overlap = self.search([
                ('id', '!=', record.id),
                ('academic_year_id', '=', year.id),
                ('date_start', '<=', record.date_end),
                ('date_end', '>=', record.date_start),
            ], limit=1)

            if overlap:
                raise ValidationError(
                    _('Periode semester bertumpang tindih dengan %s.')
                    % overlap.display_name
                )

    @api.constrains('state')
    def _check_single_active_semester(self):
        for record in self.filtered(
            lambda rec: rec.state == 'active'
        ):
            other = self.search([
                ('id', '!=', record.id),
                ('state', '=', 'active'),
            ], limit=1)

            if other:
                raise ValidationError(
                    _('Hanya boleh ada satu semester aktif. '
                      'Semester aktif saat ini: %s.')
                    % other.display_name
                )

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def action_set_active(self):
        if any(
            record.academic_year_id.state != 'active'
            for record in self
        ):
            raise ValidationError(
                _('Aktifkan tahun ajaran terlebih dahulu '
                  'sebelum mengaktifkan semester.')
            )

        self.write({'state': 'active'})

    def action_close(self):
        self.write({'state': 'closed'})
