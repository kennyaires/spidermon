from spidermon import Monitor, Rule, Action, TestCase


STATS = {
    'downloader/response_count': 63785,
    'item_scraped_count': 29836,
    'finish_reason': 'finished',
}


class DummyAction(Action):
    def run(self, result):
        pass


class MessageAction(Action):
    def __init__(self, msg):
        self.msg = msg

    def run(self, result):
        print 'RUNNING ACTION:', self.msg


#---------------------------------------------------------------
# A. Monitor from parameters
#---------------------------------------------------------------
MONITOR_A = Monitor(
    name='A. Monitor from parameters',
    rules=[
        lambda stats: stats.finish_reason == 'finished',
        lambda stats: stats['downloader/response_count'] > 10000,
    ],
    actions=[
        MessageAction('finish reason is ok!'),
    ]
)


#---------------------------------------------------------------
# B. Adding rules and actions
#---------------------------------------------------------------
MONITOR_B = Monitor(name='B. Adding rules and actions')
MONITOR_B.add_rule(rule=lambda stats: stats.finish_reason == 'finished')
MONITOR_B.add_action(action=MessageAction('finish reason is ok!'))


#---------------------------------------------------------------
# C. Monitor without rules
#---------------------------------------------------------------
MONITOR_C = Monitor(
    name='C. Monitor without rules',
    actions=[
        MessageAction('hi there!'),
    ]
)


#---------------------------------------------------------------
# D. All rule type definitions
#---------------------------------------------------------------
def rule_as_function(stats):
    return stats.finish_reason == 'finished'


class ARule(Rule):
    def check(self, stats):
        return stats.finish_reason == 'finished'


class ATestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_a(self):
        return self.stats.finish_reason == 'finished'

    def test_b(self):
        return self.stats.finish_reason == 'finished'

MONITOR_D = Monitor(
    name='D. All rule type definitions',
    rules=[
        lambda stats: stats.finish_reason == 'finished',  # lambda
        'stats.finish_reason == "finished"',  # python expression string
        rule_as_function,  # function
        ARule(),  # Rule
        ATestCase(),  # TestCase
    ],
    actions=[
        DummyAction(),
    ]
)


#---------------------------------------------------------------
# E. Naming rules and actions
#---------------------------------------------------------------
MONITOR_E = Monitor(
    name='E. Naming rules and actions',
    rules=[
        ('Rule 1', rule_as_function),
        ('Rule 2', rule_as_function),
    ],
    actions=[
        ('Action 1', DummyAction()),
    ]
)
MONITOR_E.add_rule(rule=rule_as_function, name='Rule 3')
MONITOR_E.add_action(action=DummyAction(), name='Action 2')


#---------------------------------------------------------------
# F. Rule levels and action triggers
#---------------------------------------------------------------
MONITOR_F = Monitor(
    name='F. Rule levels and action triggers',
    rules=[
        ('Rule High',   'stats.finish_reason == "finished"', 'HIGH'),
        ('Rule Normal', 'stats.finish_reason != "finished"', 'NORMAL'),
        ('Rule Low',    'stats.finish_reason != "finished"', 'LOW'),
    ],
    actions=[
        ('Action runs always',    DummyAction()),  #  trigger defaults to ALWAYS
        ('Action runs always',    DummyAction(), 'ALWAYS'),
        ('Action runs on passed', DummyAction(), 'PASSED'),
        ('Action runs on failed', DummyAction(), 'FAILED'),
        ('Action runs on error',  DummyAction(), 'ERROR'),
    ]
)
MONITOR_F.add_rule(rule=rule_as_function, name='Rule Low 2', level='LOW')
MONITOR_F.add_action(action=DummyAction(), name='Action on passed', trigger='PASSED')


#---------------------------------------------------------------
# G. Rule and Action Errors
#---------------------------------------------------------------
class BombAction(Action):
    def run(self, result):
        raise Exception('Boom!')


MONITOR_G = Monitor(
    name='G. Rule and Action Errors',
    rules=[
        'stats.a_non_existing_key == "whatever"',
    ],
    actions=[
        ('Action on error', BombAction(), 'ERROR'),
    ]
)


MONITORS = [
    MONITOR_A,
    MONITOR_B,
    MONITOR_C,
    MONITOR_D,
    MONITOR_E,
    MONITOR_F,
    MONITOR_G,
]

if __name__ == "__main__":
    for monitor in MONITORS:
        result = monitor.run(STATS)
        print result.debug()
        #print result.json()
        print '\n'*5
