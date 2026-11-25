const app = require('./app');
const createEurekaClient = require('./config/eureka');

const PORT = Number(process.env.PORT) || 8083;
const eurekaClient = createEurekaClient(PORT);

const server = app.listen(PORT, () => {
  console.log(`Meeting démarré sur le port ${PORT}`);
  eurekaClient.start((error) => {
    console.log(error ? `Erreur Eureka : ${error}` : 'MEETING enregistré dans Eureka');
  });
});

function shutdown() {
  eurekaClient.stop(() => server.close(() => process.exit(0)));
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);