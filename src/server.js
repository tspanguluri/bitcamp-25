const express = require('express');
const path = require('path');
const axios = require('axios')
const app = express();
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs');                      // Use EJS
app.set('views', path.join(__dirname, '../views')); // Adjust path if needed

app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (req, res) => {
    res.render("index")
});


app.post('/results', async (req, res) => {
    const mood = req.body.moodInput 
    const song_num = req.body.numSongs 
    const genres = req.body.genreType 
    try {
        const response = await axios.get('http://localhost:8000/chatgpt/chatgpt', {
            params: {
                "mood": mood, 
                "song_num": song_num, 
                "genres": genres 
            }
        });
        const results = response.data
        const songs = results.songs 
        console.log(results)
        console.log(songs)
        try {
            const spotify_response = await axios.post('http://localhost:8000/spotify/search-track', {
                listings: songs
            })
            console.log("\n\n")
            console.log("hello " + spotify_response)
            console.log("\n\n")
            songs_new = []
            count = 0
            for (let i = 0; i < spotify_response.data.length; i++) {
                currObj = spotify_response.data[i]
                currObj["backgroundColor"] = results.colors[count % 3]
                count += 1
                songs_new.push(currObj)
            }
            console.log(songs)
            res.render("results", {songs: songs_new})
        } catch (error_one) {
            if (error_one.response) {
              console.error("Spotify request failed:");
              console.error("Status:", error_one.response.status);
              console.error("Data:", error_one.response.data);
            } else {
              console.error("Error:", error_one.message);
            }
        }
    } catch (error) {
        console.log(error)
    }
})

// app.post('/res', (req, res)) {
//     const mood = req.body.mood; 
//     console.log('User mood is: ' + mood) 

// }

// app.get('/results', (req,res) => {
//     res.render('results')
// });

app.listen(3000, console.log("working!"))