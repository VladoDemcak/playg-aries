import express, { Express } from 'express';
import cors from 'cors';
import logger from 'aries-framework-javascript/build/lib/logger';
import bodyParser from 'body-parser';
import { Agent, InboundTransporter, OutboundTransporter, encodeInvitationToUrl } from 'aries-framework-javascript';
import { OutboundPackage } from 'aries-framework-javascript/build/lib/types';
import { MessageRepository } from 'aries-framework-javascript/build/lib/storage/MessageRepository';
import { InMemoryMessageRepository } from 'aries-framework-javascript/build/lib/storage/InMemoryMessageRepository';

const indy = require('indy-sdk');

const config = {
  url: process.env.AGENT_URL || '',
  port: process.env.AGENT_PORT || 3000,
  label: process.env.AGENT_LABEL || '',
  walletConfig: { id: process.env.WALLET_NAME || 'faber' },
  walletCredentials: { key: process.env.WALLET_KEY || 'faber-key' },
  publicDid: process.env.PUBLIC_DID || 'DPvobytTtKvmyeRTJZYjsg',
  publicDidSeed: process.env.PUBLIC_DID_SEED || '000000000000000000000000000Agent',
}


class HttpInboundTransporter implements InboundTransporter {
  app: Express;

  constructor(app: Express) {
    this.app = app;
  }

  start(agent: Agent) {
    this.app.post('/msg', async (req, res) => {
      const message = req.body;
      const packedMessage = JSON.parse(message);
      const outboundMessage = await agent.receiveMessage(packedMessage);
      if (outboundMessage) {
        res
          .status(200)
          .json(outboundMessage.payload)
          .end();
      } else {
        res.status(200).end();
      }
    });
  }
}

class StorageOutboundTransporter implements OutboundTransporter {
  messages: { [key: string]: any } = {};
  messageRepository: MessageRepository;

  constructor(messageRepository: MessageRepository) {
    this.messageRepository = messageRepository;
  }

  async sendMessage(outboundPackage: OutboundPackage) {
    const { connection, payload } = outboundPackage;

    if (!connection) {
      throw new Error(`Missing connection. I don't know how and where to send the message.`);
    }

    if (!connection.theirKey) {
      throw new Error('Trying to save message without theirKey!');
    }

    logger.logJson('Storing message', { connection, payload });

    this.messageRepository.save(connection.theirKey, payload);
  }
}

const PORT = config.port;
const app = express();

app.use(cors());
app.use(bodyParser.text());
app.set('json spaces', 2);

const messageRepository = new InMemoryMessageRepository();
const messageSender = new StorageOutboundTransporter(messageRepository);
const messageReceiver = new HttpInboundTransporter(app);
const agent = new Agent(config, messageReceiver, messageSender, indy, messageRepository);

app.get('/', async (req, res) => {
  const agentDid = agent.getPublicDid();
  res.send(agentDid);
});

// Create new invitation as inviter to invitee
app.get('/invitation', async (req, res) => {
  const connection = await agent.connections.createConnection();
  const { invitation } = connection;

  if (!invitation) {
    throw new Error('There is no invitation in newly created connection!');
  }

  const invitationUrl = encodeInvitationToUrl(invitation);
  res.send(invitationUrl);
});

app.get('/api/connections/:verkey', async (req, res) => {
  // TODO This endpoint is for testing purpose only. Return agency connection by their verkey.
  const verkey = req.params.verkey;
  const connection = await agent.connections.findConnectionByTheirKey(verkey);
  res.send(connection);
});

app.get('/api/connections', async (req, res) => {
  // TODO This endpoint is for testing purpose only. Return agency connection by their verkey.
  const connections = await agent.connections.getAll();
  res.json(connections);
});

app.get('/api/routes', async (req, res) => {
  // TODO This endpoint is for testing purpose only. Return agency connection by their verkey.
  const routes = agent.routing.getRoutingTable();
  res.send(routes);
});

app.get('/api/messages', async (req, res) => {
  // TODO This endpoint is for testing purpose only.
  res.send(messageSender.messages);
});

app.listen(PORT, async () => {
  console.log('feafea')
  await agent.init();
  messageReceiver.start(agent);
  console.log(`Application started on port ${PORT}`)
  logger.log(`Application started on port ${PORT}`);
});