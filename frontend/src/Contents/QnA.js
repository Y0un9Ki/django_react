import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { IoClose } from "react-icons/io5";
import { styled as muiStyled } from "@mui/material/styles";
import { TextField, Button } from "@mui/material";
import { MdBorderColor } from "react-icons/md";
import { FaRegListAlt } from "react-icons/fa";
import { FaRegCommentDots } from "react-icons/fa";
import { FaCommentDots } from "react-icons/fa6";
import Pagination from "@mui/material/Pagination";

const QnA = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState({ title: "", contents: "" });
  const [commentValue, setCommentValue] = useState("");
  const { title, contents } = inputValue;
  const [postStatus, setPostStatus] = useState();
  const [commentOpen, setCommentOpen] = useState(false);
  const [postsData, setPostsData] = useState([]);
  const [commentsData, setCommentsData] = useState([]);
  const [detailPost, setDetailPost] = useState();
  const [page, setPage] = useState(1);
  const pageCount = 5;

  const inputHandler = (e) => {
    const { name, value } = e.target;

    setInputValue({
      ...inputValue,
      [name]: value,
    });
  };

  const pageChange = (e, value) => {
    setPage(value);
  };

  const commentHandler = (e) => {
    setCommentValue(e.target.value);
  };

  useEffect(() => {
    fetch(`http://localhost:8000/post/post/?page=${page}`, {
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        setPostsData(res);
      });
  }, [page]);

  useEffect(() => {
    if (!postStatus) return;
    if (isOpen) {
      setIsOpen(false);
    }
    fetch(`http://localhost:8000/post/post/${postStatus}`, {
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((res) => {
        setDetailPost(res);
      });
    fetch(`http://localhost:8000/post/comments/${postStatus}`, {
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => res.json())
      .then((res) => {
        setCommentsData(res);
      });
  }, [postStatus]);

  const commentOpenHandler = () => {
    setCommentOpen(!commentOpen);
  };

  const convertDate = (d) => {
    const date = new Date(d);

    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    const formattedDate = `${year}년 ${month}월 ${day}일`;
    return formattedDate;
  };

  const postSubmitHandler = () => {
    if (!inputValue.title || !inputValue.contents) return;
    fetch("http://localhost:8000/post/post/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("SEMITOKEN")}`,
      },
      body: JSON.stringify({
        title: title,
        content: contents,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
      })
      .then((res) => {
        fetch("http://localhost:8000/post/post", {
          headers: { "Content-Type": "application/json" },
        })
          .then((res) => res.json())
          .then((res) => {
            setPostsData(res);
          });
      });
    if (isOpen) {
      setIsOpen(false);
    }
    setInputValue({ title: "", contents: "" });
  };

  const commentSubmitHandler = () => {
    if (!commentValue) return;
    fetch(`http://localhost:8000/post/comment/${postStatus}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("SEMITOKEN")}`,
      },
      body: JSON.stringify({
        post: postStatus,
        comment: commentValue,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        fetch(`http://localhost:8000/post/comments/${postStatus}`, {
          headers: { "Content-Type": "application/json" },
        })
          .then((res) => res.json())
          .then((res) => {
            setCommentsData(res);
          });
        setCommentValue("");
      });
  };
  return (
    <Container>
      <Header>
        <TitleSection>
          <Title>문의 사항</Title>
        </TitleSection>
        {!postStatus ? (
          localStorage.getItem("SEMITOKEN") ? (
            <OptionSection
              onClick={() => {
                setIsOpen(true);
              }}
            >
              <MdBorderColor size={24} style={{ cursor: "pointer" }} />
            </OptionSection>
          ) : null
        ) : (
          <OptionSection
            onClick={() => {
              setPostStatus();
            }}
          >
            <FaRegListAlt size={24} style={{ cursor: "pointer" }} />
          </OptionSection>
        )}
      </Header>
      {!postStatus ? (
        <ListsSection>
          <Lists>
            {postsData &&
              postsData.results?.map((value) => {
                return (
                  <ListContainer
                    key={value.id}
                    onClick={() => {
                      setPostStatus(value.id);
                    }}
                  >
                    <ListHeader>
                      <NameSection>작성자: {value.user}</NameSection>
                      <CreatedSection>
                        {convertDate(value.created_at)}
                      </CreatedSection>
                    </ListHeader>
                    <ListBody>{value.title}</ListBody>
                  </ListContainer>
                );
              })}
          </Lists>
          <PageSection>
            <Pagination
              count={Math.ceil(postsData?.count / pageCount)}
              onChange={pageChange}
            />
          </PageSection>
        </ListsSection>
      ) : (
        <PostSection>
          <PostContainer>
            <PostHeader>
              <PostTitle>{detailPost && detailPost.title}</PostTitle>
              <PostSubHeader>
                <PostText>{detailPost && detailPost.user}</PostText>
                <PostText>
                  {detailPost && convertDate(detailPost.created_at)}
                </PostText>
              </PostSubHeader>
            </PostHeader>
            <PostBody>{detailPost && detailPost.content}</PostBody>
            <CommentSection isOpen={commentOpen}>
              <CommentHeader>
                <CommentTitle>답글</CommentTitle>
                <CommentOpen>
                  {commentOpen ? (
                    <FaCommentDots size={28} onClick={commentOpenHandler} />
                  ) : (
                    <FaRegCommentDots size={28} onClick={commentOpenHandler} />
                  )}
                </CommentOpen>
              </CommentHeader>
              <Wrapper>
                <CommentListSection>
                  {commentsData &&
                    commentsData.data?.map((data) => {
                      return (
                        <CommentList>
                          <CommentUser>{data.user}</CommentUser>
                          <Comment>{data.comment}</Comment>
                        </CommentList>
                      );
                    })}
                </CommentListSection>
                <CommentPostSection>
                  <CommentFieldInput
                    value={commentValue}
                    onChange={commentHandler}
                  />
                  <SubmitButton
                    style={{ width: "80px", height: "46px" }}
                    onClick={commentSubmitHandler}
                  >
                    답글
                  </SubmitButton>
                </CommentPostSection>
              </Wrapper>
            </CommentSection>
          </PostContainer>
        </PostSection>
      )}
      {isOpen && (
        <Modal>
          <ModalHeader>
            <ModalTitle>문의사항</ModalTitle>
            <IoClose
              size={24}
              style={{ cursor: "pointer" }}
              onClick={() => {
                setIsOpen(false);
              }}
            />
          </ModalHeader>
          <ModalBody>
            <TextInput
              id="standard-basic"
              name="title"
              label="문의사항 제목"
              variant="standard"
              value={title}
              onChange={inputHandler}
              fullWidth
            />
            <TextFieldWrapper>
              <TextFieldLabel>문의 내용</TextFieldLabel>
              <TextFieldInput
                type="text"
                name="contents"
                value={contents}
                onChange={inputHandler}
              />
            </TextFieldWrapper>
            <ModalBottom>
              <SubmitButton onClick={postSubmitHandler}>문의하기</SubmitButton>
            </ModalBottom>
          </ModalBody>
        </Modal>
      )}
    </Container>
  );
};

export default QnA;

const Container = styled.div`
  position: relative;
  height: 80vh;
`;

const Wrapper = styled.div``;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px 20px 30px;
  border-bottom: 1px solid #bbb;
`;

const TitleSection = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
`;

const Title = styled.p`
  font-size: 20px;
`;

const OptionSection = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
  &:hover {
    background-color: #ccc;
  }
`;

const ListsSection = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  height: 650px;
  padding: 20px 30px;
`;

const Lists = styled.div`
  width: 100%;
  height: 600px;
`;

const ListContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100px;
  margin-bottom: 20px;
  border: 1px solid #aaa;
  border-radius: 8px;
  cursor: pointer;
  transition: box-shadow 0.3s ease-in-out;
  &:hover {
    animation: shadowAnimation 0.3s ease-in-out forwards;
  }

  @keyframes shadowAnimation {
    0% {
      box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.1);
    }
    100% {
      box-shadow: 0px 0px 3px rgba(0, 0, 0, 0.6);
    }
  }
`;

const PageSection = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const ListHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #aaa;
  background-color: #c6c3ba;
  border-top-right-radius: 8px;
  border-top-left-radius: 8px;
  height: 30px;
`;

const NameSection = styled.div`
  font-size: 16px;
`;

const CreatedSection = styled.div`
  font-size: 16px;
  color: #666;
`;

const ListBody = styled.div`
  display: flex;
  align-items: center;
  padding: 0 20px;
  height: 70px;
  background-color: #e8e5d9;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  font-size: 18px;
`;

const PostSection = styled.div`
  height: 660px;
  padding: 20px 30px;
`;

const PostContainer = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  border: 1px solid #aaa;
  border-radius: 8px;
  overflow: hidden;
`;
const PostHeader = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid #aaa;
  background-color: #c6c3ba;
  border-top-right-radius: 8px;
  border-top-left-radius: 8px;
  height: 80px;
`;

const PostSubHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 20px;
`;

const PostText = styled.p`
  font-size: 14;
  color: #666;
`;

const PostTitle = styled.p`
  display: flex;
  align-items: center;
  height: 40px;
  font-size: 18px;
`;

const PostBody = styled.div`
  display: flex;
  padding: 30px 20px;
  height: 610px;
  background-color: #e8e5d7;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  font-size: 18px;
`;

const CommentHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 50px;
  background-color: #c6c3ba;
  border-bottom: 1px solid #aaa;
`;

const CommentTitle = styled.p`
  font-size: 16px;
`;
const CommentOpen = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
  &:hover {
    background-color: #aaa;
  }
`;
const CommentSection = styled.div`
  position: absolute;
  width: 100%;
  height: ${({ isOpen }) => (isOpen ? "520px" : "100px")};
  background-color: #e8e5d7;
  bottom: 0;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  border-top: 1px solid #aaa;
  box-shadow: 0px -10px 10px rgba(0, 0, 0, 0.05);
  transition: height 0.2s ease-in-out, box-shadow 0.5s ease-in-out;
`;

const CommentListSection = styled.div`
  height: 400px;
  padding: 0 20px;
  overflow: scroll;
`;

const CommentList = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 40px;
  border: 1px solid #bbb;
  margin-top: 10px;
  border-radius: 4px;
  padding: 10px 0;
`;

const CommentUser = styled.div`
  display: flex;
  align-items: center;
  height: 16px;
  font-size: 14px;
  padding: 0 10px;
`;

const Comment = styled.div`
  display: flex;
  align-items: center;
  padding: 10px 0 0 10px;
  font-size: 16px;
`;

const CommentPostSection = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
  height: 60px;
  border-top: 1px solid #aaa;
`;

const CommentFieldInput = styled.textarea`
  width: 600px;
  height: 30px;
  padding: 8px;
  font-size: 16px;
  background-color: #f8f5ec;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  &:focus {
    border-color: #000;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    transition: border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  }
`;

const Modal = styled.div`
  position: absolute;
  width: 500px;
  height: 600px;
  background-color: #f8f5ec;
  top: 50%;
  left: 50%;
  transform: translate3d(-50%, -50%, 0);
  border: 1px solid #bbb;
  border-radius: 15px;
`;

const ModalHeader = styled.div`
  height: 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #e7e4db;
  border-bottom: 1px solid #bbb;
  border-radius: 15px 15px 0 0;
`;

const ModalTitle = styled.p``;

const ModalBody = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  word-wrap: break-word;
`;

const TextInput = muiStyled(TextField)(() => ({
  "& label.Mui-focused": {
    color: "#493d26",
  },
  "& .MuiInput-underline:after": {
    borderBottomColor: "#493d26",
  },
}));

const TextFieldWrapper = styled.div`
  display: flex;
  flex-direction: column;
  margin: 32px 0;
`;

const TextFieldLabel = styled.label`
  margin-bottom: 8px;
`;

const TextFieldInput = styled.textarea`
  height: 300px;
  padding: 8px;
  font-size: 16px;
  background-color: #f8f5ec;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  &:focus {
    border-color: #000;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    transition: border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  }
`;

const ModalBottom = styled.div``;

const SubmitButton = muiStyled(Button)(() => ({
  background: "#786d5f",
  color: "#ddd",
  "&: hover": {
    color: "white",
    background: "#786d5f",
  },
}));
