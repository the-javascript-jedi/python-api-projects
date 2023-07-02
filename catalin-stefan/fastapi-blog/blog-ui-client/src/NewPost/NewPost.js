import React, { useState } from "react";
import "./NewPost.css";

const BASE_URL = "http://localhost:8000/";

function NewPost() {
  const [image, setImage] = useState(null);
  const [creator, setCreator] = useState("");
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");

  const handleImageUpload = (e) => {
    if (e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  const handleCreate = (e) => {
    e?.preventDefault();
    const formData = new FormData();
    formData.append("image", image);
    const requestOptions = {
      method: "POST",
      body: formData,
    };
    fetch(BASE_URL + "post/image", requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => {
        createPost(data.filename);
      })
      .catch((error) => {
        console.log("error", error);
      })
      .finally(() => {
        setImage(null);
        document.getElementById("fileInput").value = null;
      });
  };

  const createPost = (imageUrl) => {
    // values set using class
    const json_string = JSON.stringify({
      image_url: imageUrl,
      title: title,
      content: text,
      creator: creator,
    });
    const requestOptions = {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: json_string,
    };
    fetch(BASE_URL + "post", requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => {
        window.location.reload();
        window.scrollTo(0, 0);
      })
      .catch((error) => {
        console.log("error", error);
      });
  };

  return (
    <div className="newpost_content">
      <div className="newpost_image">
        <input type="file" id="fileInput" onChange={handleImageUpload} />
      </div>
      <div className="newpost_creator">
        <input
          type="text"
          className="newpost_creator"
          id="creator_input"
          placeholder="Creator"
          onChange={(event) => {
            setCreator(event.target.value);
          }}
          value={creator}
        />
      </div>
      <div className="newpost_title">
        <input
          type="text"
          className="newpost_title"
          id="title_input"
          placeholder="Title"
          onChange={(event) => {
            setTitle(event.target.value);
          }}
          value={title}
        />
      </div>
      <div className="newpost_text">
        <textarea
          className="newpost_text"
          rows="10"
          id="content_input"
          placeholder="Content"
          onChange={(event) => {
            setText(event.target.value);
          }}
          value={text}
        />
      </div>
      <div>
        <button className="create_button" onClick={handleCreate}>
          Create
        </button>
      </div>
    </div>
  );
}
export default NewPost;
