# semana-07/app/monitoring/alerts.py
from typing import Dict, List, Callable
import asyncio
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass
import logging

@dataclass
class AlertRule:
    name: str
    metric_name: str
    threshold: float
    comparison: str  # 'gt', 'lt', 'eq'
    duration: int  # segundos
    action: Callable

class AlertManager:
    def __init__(self, domain: str):
        self.domain = domain  # 'edu_'
        self.rules: List[AlertRule] = []
        self.alert_state: Dict[str, Dict] = {}

    def add_rule(self, rule: AlertRule):
        """Añade una regla de alerta (personalizada para clases y horarios)"""
        self.rules.append(rule)
        self.alert_state[rule.name] = {
            'triggered': False,
            'last_check': 0,
            'trigger_count': 0
        }

    def check_alerts(self, metrics_data: Dict[str, float]):
      

        for rule in self.rules:
            if rule.metric_name in metrics_data:
                value = metrics_data[rule.metric_name]
                should_trigger = self._evaluate_rule(rule, value)
    def _evaluate_rule(self, rule: AlertRule, value: float) -> bool:
        """Evalúa si una regla debe disparar alerta"""
        if rule.comparison == 'gt':
            return value > rule.threshold
        elif rule.comparison == 'lt':
            return value < rule.threshold
        elif rule.comparison == 'eq':
            return value == rule.threshold
        return False

    def _handle_alert(self, rule: AlertRule, value: float, current_time: float):
        """Maneja el disparo de una alerta (ej. alta latencia en horarios)"""
        state = self.alert_state[rule.name]

        if not state['triggered']:
            state['triggered'] = True
            state['trigger_time'] = current_time

        # Verificar duración
        if current_time - state.get('trigger_time', 0) >= rule.duration:
            rule.action(rule, value)
            state['trigger_count'] += 1

    def _reset_alert(self, rule_name: str):
        """Resetea el estado de una alerta"""
        if rule_name in self.alert_state:
            self.alert_state[rule_name]['triggered'] = False

# Acciones de alerta personalizadas para Academia de Música
def email_alert(rule: AlertRule, value: float):
    """Envía alerta por email (simulada con print para pruebas)"""
    print(f"🚨 ALERTA EDU: {rule.name} - Valor: {value} (Umbral: {rule.threshold}) - Revisar horarios/clases!")

def log_alert(rule: AlertRule, value: float):
    """Registra alerta en logs"""
    logging.warning(f"Alert triggered EDU: {rule.name} - Value: {value} - Posible impacto en disponibilidad de clases")