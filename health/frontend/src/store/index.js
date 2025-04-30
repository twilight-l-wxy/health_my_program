import { configureStore } from '@reduxjs/toolkit';
import { combineReducers } from 'redux';

// 用户状态管理
const userInitialState = {
  isLoggedIn: false,
  userInfo: null,
  token: null,
};

const userReducer = (state = userInitialState, action) => {
  switch (action.type) {
    case 'USER_LOGIN':
      return {
        ...state,
        isLoggedIn: true,
        userInfo: action.payload.userInfo,
        token: action.payload.token,
      };
    case 'USER_LOGOUT':
      return userInitialState;
    case 'UPDATE_USER_INFO':
      return {
        ...state,
        userInfo: { ...state.userInfo, ...action.payload },
      };
    default:
      return state;
  }
};

// 症状自查状态管理
const symptomCheckInitialState = {
  currentStep: 0,
  symptoms: [],
  questions: [],
  answers: [],
  result: null,
  loading: false,
  error: null,
};

const symptomCheckReducer = (state = symptomCheckInitialState, action) => {
  switch (action.type) {
    case 'SET_SYMPTOMS':
      return {
        ...state,
        symptoms: action.payload,
      };
    case 'SET_QUESTIONS':
      return {
        ...state,
        questions: action.payload,
      };
    case 'ADD_ANSWER':
      return {
        ...state,
        answers: [...state.answers, action.payload],
      };
    case 'NEXT_STEP':
      return {
        ...state,
        currentStep: state.currentStep + 1,
      };
    case 'PREV_STEP':
      return {
        ...state,
        currentStep: Math.max(0, state.currentStep - 1),
      };
    case 'SET_RESULT':
      return {
        ...state,
        result: action.payload,
      };
    case 'RESET_CHECK':
      return symptomCheckInitialState;
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    default:
      return state;
  }
};

// 根reducer
const rootReducer = combineReducers({
  user: userReducer,
  symptomCheck: symptomCheckReducer,
});

// 创建store
const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== 'production',
});

export default store;