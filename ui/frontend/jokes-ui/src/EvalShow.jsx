import { useState } from 'react';

import { Container, Row, Col, Button, Carousel } from "react-bootstrap";

import MainJoke from "./MainJoke.jsx";
import "./static/carousel_arrows.css";

function EvalShow(props) {

    const [rating_cb, set_rating_cb] = useState(0);
    const [rating_svd, set_rating_svd] = useState(0);
    const [rating_random, set_rating_random] = useState(0);

    const main_joke_cb = props.visible_jokes_cb[0];
    const main_joke_svd = props.visible_jokes_svd[0];
    const main_joke_random = props.visible_jokes_random[0];

    const handle_rating_submit = async () => {
        let uid = props.uid;
        if (uid == -1)
        {
            uid = await props.handle_uid_create();
        }

        for (let recommender of ["cb", "svd", "recommender"])
        {
            let rating;
            let jid;
            if (recommender == "cb")
            {
                rating = rating_cb;
                jid = main_joke_cb[0];
            }
            else if (recommender == "svd")
            {
                rating = rating_svd;
                jid = main_joke_svd[0];
            }
            else
            {
                rating = rating_random;
                jid = main_joke_random[0];
            }

            const n_rating = Number(rating)
    
            const response = await fetch("http://127.0.0.1:5000/submit_rating", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"uid": uid, "jid": jid, "rating": n_rating})
            })
        }

        props.set_profile(
            {...props.profile,
                [main_joke_cb[0] + " cb"]: Number(rating_cb),
                [main_joke_svd[0] + " svd"]: Number(rating_svd),
                [main_joke_random[0] + " random"]: Number(rating_random),}
        );
    }

    return (
        <Container>
            <Row className="mb-3">
                <Col>
                    <Carousel interval={null} variant="dark">
                        <Carousel.Item>
                            <Col xs={{ span: 8, offset: 2 }} sm={{ span: 8, offset: 2 }} md={{ span: 8, offset: 2 }} lg={{ span: 8, offset: 2 }}>
                                <MainJoke
                                    main_joke={main_joke_cb}
                                    uid={props.uid}
                                    profile={props.profile}
                                    set_profile={props.set_profile}
                                    handle_uid_create={props.handle_uid_create}
                                    rating={rating_cb}
                                    set_rating={set_rating_cb}
                                />
                            </Col>
                        </Carousel.Item>
                        <Carousel.Item>
                            <Col xs={{ span: 8, offset: 2 }} sm={{ span: 8, offset: 2 }} md={{ span: 8, offset: 2 }} lg={{ span: 8, offset: 2 }}>
                                <MainJoke
                                    main_joke={main_joke_svd}
                                    uid={props.uid}
                                    profile={props.profile}
                                    set_profile={props.set_profile}
                                    handle_uid_create={props.handle_uid_create}
                                    rating={rating_svd}
                                    set_rating={set_rating_svd}
                                />
                            </Col>
                        </Carousel.Item>
                        <Carousel.Item>
                            <Col xs={{ span: 8, offset: 2 }} sm={{ span: 8, offset: 2 }} md={{ span: 8, offset: 2 }} lg={{ span: 8, offset: 2 }}>
                                <MainJoke
                                    main_joke={main_joke_random}
                                    uid={props.uid}
                                    profile={props.profile}
                                    set_profile={props.set_profile}
                                    handle_uid_create={props.handle_uid_create}
                                    rating={rating_random}
                                    set_rating={set_rating_random}
                                />
                            </Col>
                        </Carousel.Item>
                    </Carousel>
                </Col>
            </Row>
            <Row>
                <Col className="d-flex justify-content-center">
                    <Button
                        className="mb-3"
                        onClick={handle_rating_submit}
                    >
                        Submit ratings
                    </Button>
                </Col>
            </Row>
        </Container>
    )
}

export default EvalShow
