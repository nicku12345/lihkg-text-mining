const Discord = require("discord.js")
const client = new Discord.Client()

const token = require("./token.js")
const fs = require('fs');

client.on("ready", () => {
    console.log("Happy!")
})

client.on("message", msg => {
    data = JSON.parse(fs.readFileSync('response.json'))

    const [col1, col2] = data["col"]
    const t = data["time"]
    const [thread, reply, character] = data["counter"]

    const res = {
            embed: {
                footer: {
                    text: `Total ${thread} threads scanned`,
                },
            title: "Last updated at: " + t,
            fields: [col1, col2]
        }
    }

    if (msg.content === "$98" || msg.content === "$hot" ) {
        msg.channel.send(res)
    }
})

client.login(token)