from st2reactor.sensor.base import Sensor

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


class SlackSocketSensor(Sensor):

    def __init__(self, sensor_service, config):
        super(SlackSocketSensor, self).__init__(sensor_service=sensor_service,
                                             config=config)
        self._logger = self.sensor_service.get_logger(__name__)
        self._token = self._config['sensor']['token'] #self._config['sensor']['token']
        self._bot_token = self._config['action_token']
        self._strip_formatting = self._config['sensor'].get('strip_formatting',
                                                            False)
        self._allow_bot_messages = self._config['sensor'].get('allow_bot_messages',
                                                              False)
    
    def setup(self):
        self._app = App(token=self._token)
        @self._app.command("/ping")
        def handle_ping(ack,say):
            ack()
            say("PONG! Stackstorm socket sensor is functional...")
        self._app.command("/ping")(handle_ping)
        @self._app.command("/peekaboo")
        def handle_status(ack,command):
            ack()
            payload={
                'type': "object", 
                     'properties': {
                         'user': command["user_id"],
                     'channel': command["channel_id"],
                     'text': command["text"],
                     'command': command["command"]
                     }
            }
            self.sensor_service.dispatch(trigger="slack.peekaboo", payload=payload)
        self._app.command("/peekaboo")(handle_status)
        self._sockethandler = SocketModeHandler(self._app, self._token)
    def run(self):
        self._sockethandler.start()
    def cleanup(self):
        self._sockethandler.close()
    def add_trigger(self,trigger):
        pass
    def update_trigger(self,trigger):
        pass
    def remove_trigger(self,trigger):
        pass



## Slash command payload
# token=gIkuvaNzQIHg97ATvDxqgjtO
# &team_id=T0001
# &team_domain=example
# &enterprise_id=E0001
# &enterprise_name=Globular%20Construct%20Inc
# &channel_id=C2147483705
# &channel_name=test
# &user_id=U2147483697
# &user_name=Steve
# &command=/weather
# &text=94070
# &response_url=https://hooks.slack.com/commands/1234/5678
# &trigger_id=13345224609.738474920.8088930838d88f008e0
# &api_app_id=A123456