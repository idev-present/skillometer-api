# Import all the models, so that Base has them before being
# imported by Alembic

from app.services.dict.db_models import * # noqa
from app.services.user.db_models import * # noqa
from app.services.vacancy.db_models import * # noqa
from app.services.company.db_models import * # noqa
from app.services.applicant.db_models import * # noqa
from app.services.reply.db_models import * # noqa
from app.services.chat.db_models import * # noqa
from app.services.event.db_models import * # noqa
from app.services.reply_activity.db_models import * # noqa
