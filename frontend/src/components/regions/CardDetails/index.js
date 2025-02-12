import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { addCardReviewOperations } from "../AddCardReviewModal/redux";

import useMaterialUiFormState from "../../../utils/useMaterialUiFormState";

import {
  IN_REVIEW,
  COMPLETE,
  REVIEW_FEEDBACK,
  IN_PROGRESS,
} from "../../../constants";

function CardDetailsUnconnected({
  // project,
  // projectId,
  // cardId,
  // card,
  // topicProgressId,
  // topicProgress,
  // topicReviews,
  // projectReviews,
  // handleClose,
  cards,
  projects,
  topicProgressArray,
  projectReviews,
  topicReviews,
  authUser,

  openReviewFormModal,
  updateProjectLink,
  fetchProject,
  fetchProjectReviews,
  fetchTopicProgress,
  fetchTopicReviews,
  fetchAgileCard,
}) {
  let urlParams = useParams() || {};
  const { cardId } = urlParams;
  const card = cards && cards[cardId];

  const projectId =
    card && card.contentTypeNice === "project" && card.recruitProject;
  const project =
    !!projectId & (projects !== undefined) ? projects[projectId] : null;

  const topicProgressId =
    card && card.contentTypeNice === "topic" && card.topicProgress;
  const topicProgress =
    !!topicProgressId & (topicProgressArray !== undefined)
      ? topicProgressArray[topicProgressId]
      : null;

  React.useEffect(() => {
    if (projectId) {
      fetchProject({ projectId });
      fetchProjectReviews({ projectId });
    }

    if (topicProgressId) {
      fetchTopicProgress({ topicProgressId });
      fetchTopicReviews({ topicProgressId });
    }
    if (cardId && (card === undefined || card === null || card === {})) {
      fetchAgileCard({ cardId });
    }
  }, [
    projectId,
    fetchProject,
    fetchProjectReviews,
    topicProgressId,
    fetchTopicProgress,
    fetchTopicReviews,
    cardId,
    fetchAgileCard,
    card,
  ]);

  const [
    formState,
    { linkSubmission },
    formErrors,
    dataFromState,
  ] = useMaterialUiFormState({
    linkSubmission: {
      required: true,
    },
  });

  const handleClickUpdateProjectLink = (e) => {
    e.preventDefault();
    const { linkSubmission } = dataFromState({ state: formState });
    updateProjectLink({ linkSubmission, cardId: project.agileCard });
  };

  const handleClickAddReview = () => {
    openReviewFormModal({ cardId: project.agileCard });
  };

  const isReviewer =
    ((project || {}).reviewerUsers || []).indexOf(authUser.userId) !== -1;

  const isAssignee =
    ((project || {}).recruitUsers || []).indexOf(authUser.userId) !== -1;

  const isStaff = authUser.isStaff === 1;

  const projectCardStatus = project && project.agileCardStatus;

  const showAddReviewButton =
    (isReviewer || isStaff) &&
    [IN_REVIEW, COMPLETE, REVIEW_FEEDBACK].indexOf(projectCardStatus) !== -1;

  const showUpdateProjectLinkForm =
    isAssignee &&
    [REVIEW_FEEDBACK, IN_PROGRESS].indexOf(projectCardStatus) !== -1;

  const currentProjectReviews =
    project && projectReviews
      ? project.projectReviews
          .map((reviewId) => projectReviews[reviewId])
          .filter((review) => review !== undefined)
      : [];

  const currentTopicReviews =
    topicProgress && topicReviews
      ? topicProgress.topicReviews
          .map((reviewId) => topicReviews[reviewId])
          .filter((review) => review !== undefined)
      : [];

  const props = {
    project,
    projectId,
    cardId,
    card,
    topicProgressId,
    topicProgress,
    topicReviews: currentTopicReviews,
    projectReviews: currentProjectReviews,

    handleClickAddReview,
    showAddReviewButton,
    showUpdateProjectLinkForm,
    handleClickUpdateProjectLink,

    linkSubmission,
    formErrors,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  // const cardId = state.CardDetails.cardId;

  // const card =
  //   !!cardId & (state.Entities.cards !== undefined)
  //     ? state.Entities.cards[cardId]
  //     : null;

  // const projectId =
  //   card && card.contentTypeNice === "project" && card.recruitProject;
  // const topicProgressId =
  //   card && card.contentTypeNice === "topic" && card.topicProgress;

  // const project =
  //   !!projectId & (state.Entities.projects !== undefined)
  //     ? state.Entities.projects[projectId]
  //     : null;

  // const topicProgress =
  //   !!topicProgressId & (state.Entities.topicProgress !== undefined)
  //     ? state.Entities.topicProgress[topicProgressId]
  //     : null;

  // const projectReviews =
  //   (project !== null) &
  //   (project !== undefined) &
  //   (state.Entities.projectReviews !== undefined)
  //     ? project.projectReviews
  //         .map((reviewId) => {
  //           return state.Entities.projectReviews[reviewId];
  //         })
  //         .filter((review) => review !== undefined)
  //     : [];

  // const topicReviews =
  //   (topicProgress !== null) &
  //   (topicProgress !== undefined) &
  //   (state.Entities.topicReviews !== undefined)
  //     ? topicProgress.topicReviews
  //         .map((reviewId) => {
  //           return state.Entities.topicReviews[reviewId];
  //         })
  //         .filter((review) => review !== undefined)
  //     : [];

  return {
    // cardId,
    // card,
    // topicProgressId,
    // topicProgress,
    // project,
    // projectId,
    // projectReviews,
    // topicReviews,
    cards: state.Entities.cards,
    projects: state.Entities.projects,
    topicProgressArray: state.Entities.topicProgress,
    projectReviews: state.Entities.projectReviews,
    topicReviews: state.Entities.topicReviews,

    authUser: state.App.authUser,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchAgileCard: ({ cardId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_AGILE_CARD.operations.maybeStart({
          data: { cardId },
        })
      );
    },

    fetchProject: ({ projectId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_RECRUIT_PROJECT.operations.maybeStart({
          data: {
            projectId,
          },
        })
      );
    },

    fetchProjectReviews: ({ projectId }) => {
      dispatch(
        apiReduxApps.FETCH_RECRUIT_PROJECT_REVIEWS_PAGE.operations.maybeStart({
          data: {
            projectId,
            page: 1,
          },
        })
      );
    },

    fetchTopicProgress: ({ topicProgressId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_TOPIC_PRGRESS.operations.maybeStart({
          data: {
            topicProgressId,
          },
        })
      );
    },
    fetchTopicReviews: ({ topicProgressId }) => {
      dispatch(
        apiReduxApps.FETCH_TOPIC_PROGRESS_REVIEWS_PAGE.operations.maybeStart({
          data: {
            topicProgressId,
            page: 1,
          },
        })
      );
    },

    openReviewFormModal: ({ cardId }) => {
      dispatch(addCardReviewOperations.openCardReviewForm({ cardId }));
    },

    updateProjectLink: ({ cardId, linkSubmission }) => {
      dispatch(
        apiReduxApps.CARD_SET_PROJECT_LINK.operations.maybeStart({
          data: { cardId, linkSubmission },
        })
      );
    },
  };
};

const CardDetails = connect(
  mapStateToProps,
  mapDispatchToProps
)(CardDetailsUnconnected);

export default CardDetails;
