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
    t = data["time"]

    const embed = {
        embed: {
            title: "Time: " + t,
            fields: [col1, col2]
        }
    }

    if (msg.content === "$98") {
        msg.channel.send(embed)
    }
})

client.login(token)