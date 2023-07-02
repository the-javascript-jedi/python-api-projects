import "./App.css";
import React, { useEffect, useState } from "react";
import Post from "./Post/Post";
import NewPost from "./NewPost/NewPost";

const BASE_URL = "http://localhost:8000/";

function App() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(BASE_URL + "post/all")
      .then((response) => {
        const json = response.json();
        console.log("json", json);
        if (response.ok) {
          return json;
        }
        // if error
        throw response;
      })
      // if no error and response has data, reverse the data to show last data first
      .then((data) => {
        return data.reverse();
      })
      // set state from response data
      .then((data) => {
        setPosts(data);
      })
      // catach error
      .catch((error) => {
        console.log("error", error);
        alert(error);
      });
  }, []);

  return (
    <div className="App">
      <div className="blog_title">Open City Blog</div>
      <div className="app_posts">
        {posts.map((post, index) => {
          return <Post post={post} key={index} />;
        })}
      </div>
      <div className="new_post">
        <NewPost />
      </div>
    </div>
  );
}

export default App;
