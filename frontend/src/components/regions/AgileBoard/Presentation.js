import React from "react";

import { makeStyles } from "@material-ui/core/styles";

import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";

import AgileCard from "./AgileCard";
import Loading from "../../widgets/Loading";

// import MarkSingleCardAttendanceModal from "../MarkSingleCardAttendanceModal";
import { Divider } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  grid: {
    display: "nowrap",
    "& > *": {
      margin: theme.spacing(1),
    },
    width: "100%",
  },

  column: {
    overflowY: "scroll",
  },
}));

export default ({
  board,
  cards,
  handleColumnScroll,
  userId,
  viewedUser,
  columnsLoading,
}) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      {/* <Typography>{user.email}</Typography> */}
      <Grid container wrap="nowrap">
        {board.map((column) => {
          return (
            <React.Fragment key={column.label}>
              <Grid
                item
                xs={"auto"}
                className={classes.grid}
                key={column.label}
              >
                <Paper elevation={3}>
                  <Typography variant="h5" align="center">
                    {column.label}
                  </Typography>
                  <div
                    className={classes.column}
                    onScroll={handleColumnScroll({ column })}
                  >
                    {column.cards.map((cardId, index) => {
                      return (
                        <AgileCard
                          key={cardId}
                          card={cards[cardId]}
                          filterUserId={userId}
                          viewedUser={viewedUser}
                        />
                      );
                    })}
                    {columnsLoading.includes(column.label) && <Loading />}
                    <Divider />
                  </div>
                </Paper>
              </Grid>
            </React.Fragment>
          );
        })}
      </Grid>
    </React.Fragment>
  );
};
