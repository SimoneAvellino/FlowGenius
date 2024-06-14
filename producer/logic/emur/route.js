const express = require('express');

const router = express.Router();
const controller = require('./controller');

router.post('/simulation/start', controller.start_simulation);
router.post('/simulation/stop', controller.stop_simulation);

module.exports = router;