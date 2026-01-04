import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

export const askQuestion = async (question) => {
  const res = await API.post("/api/ask", {
    question,
    top_k: 5
  });
  return res.data;
};
