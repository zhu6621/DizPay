# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import pickle
import SocketServer
import struct


class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            payload = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(payload)
            while len(chunk) < payload:
                chunk = chunk + self.connection.recv(payload - len(chunk))
            record = logging.makeLogRecord(pickle.loads(chunk))
            self.handle_log_record(record)

    def handle_log_record(self, record):
        logger = self.server.logger
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT + 101,
                 handler=LogRecordStreamHandler):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        path = '/var/log/icaiquan-api'
        if not os.path.exists(path):
            os.mkdir(path)
        log_file = os.path.join(path, 'icaiquan-api.log')
        log_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=7)
        formatter = '[%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s] %(message)s'
        log_handler.setFormatter(logging.Formatter(formatter))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(log_handler)

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


def main():
    log_server = LogRecordSocketReceiver()
    log_server.serve_until_stopped()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
