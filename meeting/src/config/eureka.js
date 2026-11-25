const { Eureka } = require('eureka-js-client');

module.exports = function createEurekaClient(port) {
    return new Eureka({
        instance: {
            app: 'meeting',                       // devient MEETING dans le dashboard
            instanceId: `meeting:${port}`,        // unique par instance
            hostName: 'localhost',
            ipAddr: '127.0.0.1',
            port: { '$': port, '@enabled': true },
            vipAddress: 'meeting',
            statusPageUrl: `http://localhost:${port}/api/meetings/hello`,
            dataCenterInfo: {
                '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
                name: 'MyOwn',
            },
        },
        eureka: {
            host: 'localhost',
            port: 8761,
            servicePath: '/eureka/apps/',
        },
    });
};