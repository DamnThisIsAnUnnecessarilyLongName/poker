import streamlit as st
import pandas as pd
import random
import polars as pl

## functions
import random
from treys import Card, Deck, Evaluator

def compute_equity(player_hand, flop_cards, num_simulations, num_opponents):
    """
    Compute the equity of a hand using Monte Carlo simulation with treys.
    
    Parameters:
    - player_hand: list of 2 card strings, e.g., ['As', 'Kd']
    - flop_cards: list of 3 card strings, e.g., ['2h', '7c', 'Td']
    - num_simulations: number of simulations to run
    - num_opponents: number of opponents
    
    Returns:
    - equity (float between 0 and 1)
    """
    evaluator = Evaluator()
    player_hand_int = [Card.new(card) for card in player_hand]
    flop_int = [Card.new(card) for card in flop_cards]

    wins = 0

    for _ in range(num_simulations):
        # Create and shuffle a fresh deck
        deck = Deck()
        
        # Remove known cards
        for card in player_hand_int + flop_int:
            deck.cards.remove(card)

        # Deal remaining board (2 more cards)
        remaining_board = deck.draw(2)
        board = flop_int + remaining_board

        # Deal opponent hands
        opponent_hands = [deck.draw(2) for _ in range(num_opponents)]

        # Evaluate hands
        player_score = evaluator.evaluate(board, player_hand_int)
        best_opponent_score = min(evaluator.evaluate(board, opp_hand) for opp_hand in opponent_hands)

        if player_score < best_opponent_score:
            wins += 1
        elif player_score == best_opponent_score:
            wins += 0.5  # account for tie

    equity = round((wins / num_simulations) * 100)
    return equity

## Extract data
df = pl.read_csv('poker_equity_problems.csv')

#----------------------------------------------------------------#
st.title("Poker post-flop trainer")

st.sidebar.title("Stats")
# Initialize counter in session_state
if 'error_margin' not in st.session_state:
    st.session_state.error_margin = []
# if 'wrong' not in st.session_state:
#     st.session_state.wrong = 0

q1, q2, q3, q4, q5 = st.tabs(["q1", "q2", "q3", "q4", "q5"])

with q1:

    ## Take problem
    if 'row_num1' not in st.session_state:
        st.session_state.row_num1 = random.randrange(0, 500)
        
    if 'opp_num1' not in st.session_state:
        st.session_state.opp_num1 = random.randrange(1,5)

    st.text(f"Problem Number: {st.session_state.row_num1}")

    st.text(f"Num of Opponents: {st.session_state.opp_num1}")

    # Player cards
    playercard1_1 = df.row(st.session_state.row_num1)[0]
    playercard2_1 = df.row(st.session_state.row_num1)[1]
    flop1_1 = df.row(st.session_state.row_num1)[2]
    flop2_1 = df.row(st.session_state.row_num1)[3]
    flop3_1 = df.row(st.session_state.row_num1)[4]
    equity_1 = compute_equity(
        [playercard1_1[:-4], playercard2_1[:-4]],
        [flop1_1[:-4], 
        flop2_1[:-4], 
        flop3_1[:-4]],
        10000,st.session_state.opp_num1)

    'Flop:'
    # Create two columns
    f_con1, f_con2, f_con3, f_con4, f_con5, f_con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with f_con1:
        st.image("images/" + flop1_1, use_container_width=True)

    with f_con2:
        st.image("images/" + flop2_1, use_container_width=True)

    with f_con3:
        st.image("images/" + flop3_1, use_container_width=True)


    'My hand:'
    # Create two columns
    con1, con2, con3, con4, con5, con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with con1:
        st.image("images/" + playercard1_1, use_container_width=True)

    with con2:
        st.image("images/" + playercard2_1, use_container_width=True)


    with st.form("percentage_form"):
        percent = st.slider("Equity", 0, 100, 0, step=10)
        submitted = st.form_submit_button("Confirm")

    if submitted:
        st.write(f"You selected: {percent}%")
        st.session_state.error_margin.append(abs(percent - equity_1))
        if abs(percent - equity_1) < 10:
            st.success(f"Actual Equity: {equity_1} %")
        else:
            st.error(f"Actual Equity: {equity_1} %")

with q2:

    ## Take problem
    if 'row_num2' not in st.session_state:
        st.session_state.row_num2 = random.randrange(0, 500)

    if 'opp_num2' not in st.session_state:
        st.session_state.opp_num2 = random.randrange(1,5)

    st.text(f"Num of Opponents: {st.session_state.opp_num2}")

    st.text(f"Problem Number: {st.session_state.row_num2}")

    # Player cards
    playercard1_1 = df.row(st.session_state.row_num2)[0]
    playercard2_1 = df.row(st.session_state.row_num2)[1]
    flop1_1 = df.row(st.session_state.row_num2)[2]
    flop2_1 = df.row(st.session_state.row_num2)[3]
    flop3_1 = df.row(st.session_state.row_num2)[4]
    equity_1 = compute_equity(
        [playercard1_1[:-4], playercard2_1[:-4]],
        [flop1_1[:-4], 
        flop2_1[:-4], 
        flop3_1[:-4]],
        10000,st.session_state.opp_num2)


    'Flop:'
    # Create two columns
    f_con1, f_con2, f_con3, f_con4, f_con5, f_con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with f_con1:
        st.image("images/" + flop1_1, use_container_width=True)

    with f_con2:
        st.image("images/" + flop2_1, use_container_width=True)

    with f_con3:
        st.image("images/" + flop3_1, use_container_width=True)


    'My hand:'
    # Create two columns
    con1, con2, con3, con4, con5, con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with con1:
        st.image("images/" + playercard1_1, use_container_width=True)

    with con2:
        st.image("images/" + playercard2_1, use_container_width=True)

    with st.form("percentage_form2"):
        percent = st.slider("Equity", 0, 100, 0, step=10)
        submitted = st.form_submit_button("Confirm")

    if submitted:
        st.write(f"You selected: {percent}%")
        st.session_state.error_margin.append(abs(percent - equity_1))
        if abs(percent - equity_1) < 10:
            st.success(f"Actual Equity: {equity_1} %")
        else:
            st.error(f"Actual Equity: {equity_1} %")

with q3:

    ## Take problem
    if 'row_num3' not in st.session_state:
        st.session_state.row_num3 = random.randrange(0, 500)

    if 'opp_num3' not in st.session_state:
        st.session_state.opp_num3 = random.randrange(1,5)

    st.text(f"Num of Opponents: {st.session_state.opp_num3}")

    st.text(f"Problem Number: {st.session_state.row_num3}")

    # Player cards
    playercard1_1 = df.row(st.session_state.row_num3)[0]
    playercard2_1 = df.row(st.session_state.row_num3)[1]
    flop1_1 = df.row(st.session_state.row_num3)[2]
    flop2_1 = df.row(st.session_state.row_num3)[3]
    flop3_1 = df.row(st.session_state.row_num3)[4]
    equity_1 = compute_equity(
        [playercard1_1[:-4], playercard2_1[:-4]],
        [flop1_1[:-4], 
        flop2_1[:-4], 
        flop3_1[:-4]],
        10000,st.session_state.opp_num3)


    'Flop:'
    # Create two columns
    f_con1, f_con2, f_con3, f_con4, f_con5, f_con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with f_con1:
        st.image("images/" + flop1_1, use_container_width=True)

    with f_con2:
        st.image("images/" + flop2_1, use_container_width=True)

    with f_con3:
        st.image("images/" + flop3_1, use_container_width=True)


    'My hand:'
    # Create two columns
    con1, con2, con3, con4, con5, con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with con1:
        st.image("images/" + playercard1_1, use_container_width=True)

    with con2:
        st.image("images/" + playercard2_1, use_container_width=True)

    with st.form("percentage_form3"):
        percent = st.slider("Equity", 0, 100, 0, step=10)
        submitted = st.form_submit_button("Confirm")

    if submitted:
        st.write(f"You selected: {percent}%")
        st.session_state.error_margin.append(abs(percent - equity_1))
        if abs(percent - equity_1) < 10:
            st.success(f"Actual Equity: {equity_1} %")
        else:
            st.error(f"Actual Equity: {equity_1} %")

with q4:

    ## Take problem
    if 'row_num4' not in st.session_state:
        st.session_state.row_num4 = random.randrange(0, 500)

    if 'opp_num4' not in st.session_state:
        st.session_state.opp_num4 = random.randrange(1,5)

    st.text(f"Num of Opponents: {st.session_state.opp_num4}")

    st.text(f"Problem Number: {st.session_state.row_num4}")

    # Player cards
    playercard1_1 = df.row(st.session_state.row_num4)[0]
    playercard2_1 = df.row(st.session_state.row_num4)[1]
    flop1_1 = df.row(st.session_state.row_num4)[2]
    flop2_1 = df.row(st.session_state.row_num4)[3]
    flop3_1 = df.row(st.session_state.row_num4)[4]
    equity_1 = compute_equity(
        [playercard1_1[:-4], playercard2_1[:-4]],
        [flop1_1[:-4], 
        flop2_1[:-4], 
        flop3_1[:-4]],
        10000,st.session_state.opp_num4)


    'Flop:'
    # Create two columns
    f_con1, f_con2, f_con3, f_con4, f_con5, f_con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with f_con1:
        st.image("images/" + flop1_1, use_container_width=True)

    with f_con2:
        st.image("images/" + flop2_1, use_container_width=True)

    with f_con3:
        st.image("images/" + flop3_1, use_container_width=True)


    'My hand:'
    # Create two columns
    con1, con2, con3, con4, con5, con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with con1:
        st.image("images/" + playercard1_1, use_container_width=True)

    with con2:
        st.image("images/" + playercard2_1, use_container_width=True)

    with st.form("percentage_form4"):
        percent = st.slider("Equity", 0, 100, 0, step=10)
        submitted = st.form_submit_button("Confirm")

    if submitted:
        st.write(f"You selected: {percent}%")
        st.session_state.error_margin.append(abs(percent - equity_1))
        if abs(percent - equity_1) < 10:
            st.success(f"Actual Equity: {equity_1} %")
        else:
            st.error(f"Actual Equity: {equity_1} %")

with q5:

    ## Take problem
    if 'row_num5' not in st.session_state:
        st.session_state.row_num5 = random.randrange(0, 500)

    if 'opp_num5' not in st.session_state:
        st.session_state.opp_num5 = random.randrange(1,5)

    st.text(f"Num of Opponents: {st.session_state.opp_num5}")

    st.text(f"Problem Number: {st.session_state.row_num5}")

    # Player cards
    playercard1_1 = df.row(st.session_state.row_num5)[0]
    playercard2_1 = df.row(st.session_state.row_num5)[1]
    flop1_1 = df.row(st.session_state.row_num5)[2]
    flop2_1 = df.row(st.session_state.row_num5)[3]
    flop3_1 = df.row(st.session_state.row_num5)[4]
    equity_1 = compute_equity(
        [playercard1_1[:-4], playercard2_1[:-4]],
        [flop1_1[:-4], 
        flop2_1[:-4], 
        flop3_1[:-4]],
        10000,st.session_state.opp_num5)


    'Flop:'
    # Create two columns
    f_con1, f_con2, f_con3, f_con4, f_con5, f_con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with f_con1:
        st.image("images/" + flop1_1, use_container_width=True)

    with f_con2:
        st.image("images/" + flop2_1, use_container_width=True)

    with f_con3:
        st.image("images/" + flop3_1, use_container_width=True)


    'My hand:'
    # Create two columns
    con1, con2, con3, con4, con5, con6 = st.columns([1, 1, 1, 1, 1, 1])

    # Text input for image path
    with con1:
        st.image("images/" + playercard1_1, use_container_width=True)

    with con2:
        st.image("images/" + playercard2_1, use_container_width=True)

    with st.form("percentage_form5"):
        percent = st.slider("Equity", 0, 100, 0, step=10)
        submitted = st.form_submit_button("Confirm")

    if submitted:
        st.write(f"You selected: {percent}%")
        st.session_state.error_margin.append(abs(percent - equity_1))
        if abs(percent - equity_1) < 10:
            st.success(f"Actual Equity: {equity_1} %")
        else:
            st.error(f"Actual Equity: {equity_1} %")

# Display running average
if st.session_state.error_margin:
    total = sum(st.session_state.error_margin)
    count = len(st.session_state.error_margin)
    average = total / count
    st.sidebar.markdown(f"% errors: {st.session_state.error_margin}")
    st.sidebar.markdown(f"% avg error: {average}")
else:
    st.write("No numbers entered yet.")
