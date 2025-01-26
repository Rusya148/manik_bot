from handlers.start import register_handlers as register_start_handlers
from handlers.rec_client import register_handlers as register_rec_client_handlers
from handlers.handler_back_buttons import register_handlers as register_callback_handlers
from handlers.clients_request_date import register_handlers as register_request_date
from handlers.delete_client import register_delete_client as register_delete
from handlers.salary import register_salary

def register(dp):
    register_start_handlers(dp)
    register_rec_client_handlers(dp)
    register_callback_handlers(dp)
    register_request_date(dp)
    register_delete(dp)
    register_salary(dp)

