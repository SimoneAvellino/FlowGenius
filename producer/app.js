const app = require('./config/express');
const emurRoute = require('./logic/emur/route');
const dotenv = require('dotenv');

dotenv.config();

const PORT = process.env.PORT;

app.use('/emur', emurRoute);

app.listen(PORT, async () => {
    console.log(`Server listening on port ${PORT}`);
    console.log(process.env)
});