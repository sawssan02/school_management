# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Schedule(models.Model):
    _name = 'school.schedule'
    _description = 'Emploi du temps'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'day_of_week, start_time'

    # Relations
    class_id = fields.Many2one('school.class', string='Classe', required=True, tracking=True)
    course_id = fields.Many2one('school.course', string='Cours', required=True, tracking=True)
    teacher_id = fields.Many2one('school.teacher', string='Enseignant', required=True, tracking=True)
    
    # Jour et horaires
    day_of_week = fields.Selection([
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
        ('sunday', 'Dimanche'),
    ], string='Jour', required=True, tracking=True)
    
    start_time = fields.Float(string='Heure de début', required=True, tracking=True)
    end_time = fields.Float(string='Heure de fin', required=True, tracking=True)
    duration = fields.Float(string='Durée (heures)', compute='_compute_duration', store=True)
    
    # Salle
    room = fields.Char(string='Salle', tracking=True)
    
    # Période
    start_date = fields.Date(string='Date de début', required=True, default=fields.Date.today)
    end_date = fields.Date(string='Date de fin')
    
    # Type de cours
    session_type = fields.Selection([
        ('lecture', 'Cours magistral'),
        ('tutorial', 'TD'),
        ('practical', 'TP'),
        ('exam', 'Examen'),
    ], string='Type de session', default='lecture')
    
    # Notes
    notes = fields.Text(string='Notes')
    
    # Actif
    active = fields.Boolean(string='Actif', default=True)
    
    # Nom affiché
    display_name = fields.Char(string='Nom', compute='_compute_display_name', store=True)
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            record.duration = record.end_time - record.start_time
    
    @api.depends('day_of_week', 'start_time', 'course_id')
    def _compute_display_name(self):
        for record in self:
            day_names = dict(self._fields['day_of_week'].selection)
            day = day_names.get(record.day_of_week, '')
            course = record.course_id.name if record.course_id else ''
            start = self._format_time(record.start_time)
            record.display_name = f"{day} {start} - {course}"
    
    def _format_time(self, time_float):
        """Convertir un float (ex: 9.5) en format heure (ex: '09:30')"""
        hours = int(time_float)
        minutes = int((time_float - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    @api.constrains('start_time', 'end_time')
    def _check_time(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError(_("L'heure de fin doit être après l'heure de début."))
            if record.start_time < 0 or record.start_time >= 24:
                raise ValidationError(_("L'heure de début doit être entre 0 et 24."))
            if record.end_time < 0 or record.end_time > 24:
                raise ValidationError(_("L'heure de fin doit être entre 0 et 24."))
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("La date de fin doit être après la date de début."))
    
    @api.constrains('class_id', 'teacher_id', 'day_of_week', 'start_time', 'end_time')
    def _check_conflicts(self):
        """Vérifie les conflits d'horaire pour la classe et l'enseignant"""
        for record in self:
            # Vérifier les conflits pour la classe
            conflict = self.search([
                ('id', '!=', record.id),
                ('class_id', '=', record.class_id.id),
                ('day_of_week', '=', record.day_of_week),
                ('active', '=', True),
                '|',
                '&', ('start_time', '<=', record.start_time), ('end_time', '>', record.start_time),
                '&', ('start_time', '<', record.end_time), ('end_time', '>=', record.end_time),
            ])
            if conflict:
                raise ValidationError(_("Conflit d'horaire détecté pour la classe %s.") % record.class_id.name)
            
            # Vérifier les conflits pour l'enseignant
            conflict = self.search([
                ('id', '!=', record.id),
                ('teacher_id', '=', record.teacher_id.id),
                ('day_of_week', '=', record.day_of_week),
                ('active', '=', True),
                '|',
                '&', ('start_time', '<=', record.start_time), ('end_time', '>', record.start_time),
                '&', ('start_time', '<', record.end_time), ('end_time', '>=', record.end_time),
            ])
            if conflict:
                raise ValidationError(_("Conflit d'horaire détecté pour l'enseignant %s.") % record.teacher_id.name)
