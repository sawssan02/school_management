# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class Student(models.Model):
    _name = 'school.student'
    _description = 'Étudiant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Informations de base
    name = fields.Char(string='Nom complet', required=True, tracking=True)
    registration_number = fields.Char(
        string='Matricule', 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: _('New'),
        tracking=True
    )
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Téléphone')
    mobile = fields.Char(string='Mobile')
    
    # Informations personnelles
    date_of_birth = fields.Date(string='Date de naissance', tracking=True)
    age = fields.Integer(string='Âge', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Masculin'),
        ('female', 'Féminin'),
        ('other', 'Autre')
    ], string='Genre', tracking=True)
    
    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-')
    ], string='Groupe sanguin')
    
    nationality = fields.Many2one('res.country', string='Nationalité')
    
    # Adresse
    street = fields.Char(string='Rue')
    street2 = fields.Char(string='Rue 2')
    city = fields.Char(string='Ville')
    state_id = fields.Many2one('res.country.state', string='État')
    zip = fields.Char(string='Code postal')
    country_id = fields.Many2one('res.country', string='Pays')
    
    # Informations académiques
    class_id = fields.Many2one('school.class', string='Classe', tracking=True)
    admission_date = fields.Date(string="Date d'admission", default=fields.Date.today, tracking=True)
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('graduated', 'Diplômé'),
        ('suspended', 'Suspendu'),
        ('expelled', 'Exclu')
    ], string='Statut', default='draft', tracking=True)
    
    # Relations
    guardian_name = fields.Char(string='Nom du tuteur')
    guardian_phone = fields.Char(string='Téléphone du tuteur')
    guardian_email = fields.Char(string='Email du tuteur')
    guardian_relation = fields.Char(string='Relation avec le tuteur')
    
    # Notes et présence
    grade_ids = fields.One2many('school.grade', 'student_id', string='Notes')
    attendance_ids = fields.One2many('school.attendance', 'student_id', string='Présences')
    
    # Statistiques
    average_grade = fields.Float(string='Moyenne générale', compute='_compute_average_grade', store=True)
    attendance_rate = fields.Float(string="Taux de présence", compute='_compute_attendance_rate', store=True)
    
    # Image
    image = fields.Binary(string='Photo')
    
    # Notes
    notes = fields.Text(string='Notes internes')
    
    # Actif
    active = fields.Boolean(string='Actif', default=True)
    
    @api.model
    def create(self, vals):
        if vals.get('registration_number', _('New')) == _('New'):
            vals['registration_number'] = self.env['ir.sequence'].next_by_code('school.student') or _('New')
        return super(Student, self).create(vals)
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                record.age = today.year - record.date_of_birth.year - (
                    (today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day)
                )
            else:
                record.age = 0
    
    @api.depends('grade_ids.grade')
    def _compute_average_grade(self):
        for record in self:
            if record.grade_ids:
                total = sum(record.grade_ids.mapped('grade'))
                record.average_grade = total / len(record.grade_ids)
            else:
                record.average_grade = 0.0
    
    @api.depends('attendance_ids')
    def _compute_attendance_rate(self):
        for record in self:
            if record.attendance_ids:
                present = len(record.attendance_ids.filtered(lambda a: a.status == 'present'))
                total = len(record.attendance_ids)
                record.attendance_rate = (present / total) * 100 if total > 0 else 0.0
            else:
                record.attendance_rate = 0.0
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not '@' in record.email:
                    raise ValidationError(_("L'adresse email n'est pas valide."))
    
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth:
                if record.date_of_birth > date.today():
                    raise ValidationError(_("La date de naissance ne peut pas être dans le futur."))
    
    def action_set_active(self):
        self.write({'status': 'active'})
    
    def action_set_graduated(self):
        self.write({'status': 'graduated'})
    
    def action_set_suspended(self):
        self.write({'status': 'suspended'})
