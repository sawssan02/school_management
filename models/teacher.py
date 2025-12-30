# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Enseignant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Informations de base
    name = fields.Char(string='Nom complet', required=True, tracking=True)
    employee_number = fields.Char(
        string='Matricule', 
        required=True, 
        copy=False, 
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    email = fields.Char(string='Email', required=True, tracking=True)
    phone = fields.Char(string='Téléphone')
    mobile = fields.Char(string='Mobile')
    
    # Informations personnelles
    date_of_birth = fields.Date(string='Date de naissance')
    gender = fields.Selection([
        ('male', 'Masculin'),
        ('female', 'Féminin'),
        ('other', 'Autre')
    ], string='Genre', tracking=True)
    
    nationality = fields.Many2one('res.country', string='Nationalité')
    
    # Adresse
    street = fields.Char(string='Rue')
    street2 = fields.Char(string='Rue 2')
    city = fields.Char(string='Ville')
    state_id = fields.Many2one('res.country.state', string='État')
    zip = fields.Char(string='Code postal')
    country_id = fields.Many2one('res.country', string='Pays')
    
    # Informations professionnelles
    hire_date = fields.Date(string="Date d'embauche", default=fields.Date.today, tracking=True)
    department = fields.Char(string='Département')
    specialization = fields.Char(string='Spécialisation')
    qualification = fields.Selection([
        ('bachelor', 'Licence'),
        ('master', 'Master'),
        ('phd', 'Doctorat'),
        ('other', 'Autre')
    ], string='Diplôme')
    
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('on_leave', 'En congé'),
        ('terminated', 'Terminé')
    ], string='Statut', default='draft', tracking=True)
    
    # Relations
    course_ids = fields.One2many('school.course', 'teacher_id', string='Cours')
    schedule_ids = fields.One2many('school.schedule', 'teacher_id', string='Emploi du temps')
    
    # Statistiques
    total_courses = fields.Integer(string='Nombre de cours', compute='_compute_total_courses', store=True)
    
    # Image
    image = fields.Binary(string='Photo')
    
    # Notes
    notes = fields.Text(string='Notes internes')
    
    # Actif
    active = fields.Boolean(string='Actif', default=True)
    
    @api.model
    def create(self, vals):
        if vals.get('employee_number', _('New')) == _('New'):
            vals['employee_number'] = self.env['ir.sequence'].next_by_code('school.teacher') or _('New')
        return super(Teacher, self).create(vals)
    
    @api.depends('course_ids')
    def _compute_total_courses(self):
        for record in self:
            record.total_courses = len(record.course_ids)
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not '@' in record.email:
                    raise ValidationError(_("L'adresse email n'est pas valide."))
    
    def action_set_active(self):
        self.write({'status': 'active'})
    
    def action_set_on_leave(self):
        self.write({'status': 'on_leave'})
