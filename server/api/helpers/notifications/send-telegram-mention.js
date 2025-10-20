/*!
 * Copyright (c) 2024 PLANKA Software GmbH
 * Licensed under the Fair Use License: https://github.com/plankanban/planka/blob/master/LICENSE.md
 */

const axios = require('axios');

module.exports = {
  inputs: {
    chatId: {
      type: 'string',
      required: true,
    },
    message: {
      type: 'string',
      required: true,
    },
  },

  async fn(inputs) {
    const { chatId, message } = inputs;
    const botUrl = 'http://telegram-bot:8080/notify'; // Assuming the bot runs on this address in the docker network

    try {
      await axios.post(botUrl, {
        chat_id: chatId,
        message,
      });
      sails.log.info(`Sent Telegram mention notification to chat ID: ${chatId}`);
    } catch (error) {
      sails.log.error(`Failed to send Telegram mention notification to chat ID: ${chatId}`, error.message);
    }
  },
};
