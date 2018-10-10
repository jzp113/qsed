from qsObject import Portfolio
from event.eventType import EVENT_SIGNAL, EVENT_TARGET_POSITION
from event.eventEngine import Event


class CtaNaivePortfolio(Portfolio):
    """
    CTA Naive Portfolio

    1. identifier_multiplier
    {
        identifier: lots_multiplier
    }

    2. symbol_mulitplier
    {
        'XBTUSD': 1,
        'ETHUSD': 0.5,
    }
    """

    def __init__(self):
        self.identifier_multiplier = {}        # {'EmaStrategy_XBTUSD_15s_9999': 98, 'EmaStrategy_XBTUSD_15s_8888': 100}
        self.symbol_multiplier = {}            # {'XBTUSD': 1.0, 'ETHUSD': 1.0}
        self.identifier_target_position = {}   # {'EmaStrategy_XBTUSD_15s_9999': -1, 'EmaStrategy_XBTUSD_15s_8888': 0}
        self.target_position = {}              # {'XBTUSD': 198, 'ETHUSD':35}

    def config(self, identifier_multiplier, symbol_multiplier):
        self.identifier_multiplier = identifier_multiplier
        self.symbol_multiplier = symbol_multiplier

    def on_signal_event(self, event):
        assert isinstance(event, Event), '__class__ is %s' % event.__class__
        assert event.type_ == EVENT_SIGNAL
        self.__update_target_position(event.dict_)
        self.__push_target_position_event()
        print('Called on_signal_event 🎲  %s' % event)

    def __update_target_position(self, dict_):
        # dict_={'target_position': -1, 'identifier': 'EmaStrategy_XBTUSD_15s_9999', 'symbol': 'XBTUSD'}
        identifier = dict_['identifier']
        symbol = dict_['symbol']
        pos = dict_['target_position']
        if identifier in self.identifier_multiplier:
            self.identifier_target_position[identifier] = pos
        if symbol in self.symbol_multiplier:
            self.target_position[symbol] = pos * self.identifier_multiplier[identifier] * self.symbol_multiplier[symbol]

    def __push_target_position_event(self):
        e = Event(type_=EVENT_TARGET_POSITION)
        e.dict_ = self.target_position
        self.event_engine.put(e)
        print('🌈 🌈 🌈  push target_position_event 🌈 🌈 🌈  %s' % e)

