// alert.js
import Swal from 'sweetalert2';
import moment from 'moment';

export const ICON_TYPES ={
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
  QUESTION: 'question',
};

export const BID_STATUS = {
  REGISTERED: 15,
  IN_PROGRESS: 16,
  AWARDED: 18,
  REJECTED: 17,
};

export const MEMBER_STATUS = {
  GENERAL_MEMBER: 1,  
  PEDNDNG_AUCTION_MEMBER: 2, 
  APPROVED_AUCTON_MEMBER: 3,
};


export function showAlert(titleMessage, btnText) {
  return Swal.fire({
    title: titleMessage,
    confirmButtonColor: "#3085d6",
    confirmButtonText: btnText,
    width: 350,
  });
}

export function showAlertWithIcon(title, textMessage, icon, showCancelButton, cancelButtonText = "No") {
  return Swal.fire({
    title,
    text: textMessage,
    icon,
    showCancelButton,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes',
    cancelButtonText
    });
}
export const NumbersEngOnly = (e) => {
    // return e.target.value.replace(/[^a-zA-Z0-9]/g, '');
    let no = e.target.value.replace(/[^a-zA-Z0-9]/g, '');
    e.target.value = no
}

export const formatDate = (dateString) => {
  return new moment(dateString).format('YYYY-MM-DD hh:mm')
}

export const formatDateYMD = (dateString) => {
  return new moment(dateString).format('YYYY-MM-DD')
}
export const format = (date) => {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();
  return `${year}-${month}-${day}`;
};
export const withBrTags = (text) => {
  if (text != undefined)
      return text.replace(/(?:\r\n|\r|\n)/g, '<br>')
}

export const filterComma = (val) => {
  let t = '0'
  val = parseFloat(val).toFixed(2).replace(/\.00$/, '')
  t = val.toString().replace(/\D/g, "")
      .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return t + '원'
}

export const separateTextBySpace = (text) => {
  return text.split('').filter(char => char !== ' ');
}

export const NumbersEngHanOnly = (e) => {
  let charLimit = e.target.maxLength;
  let sanitizedValue = e.target.value.replace(/[^a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣.\n]/g, '');
  sanitizedValue = sanitizedValue.slice(0, charLimit); // Limit the number of characters
  e.target.value = sanitizedValue //e.target.value.replace(/[^a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣.\n]/g, '');
}

export const NumbersOnly = (e) => {
    let no = e.target.value.replace(/[^0-9]/g, '')
    e.target.value = no
    // return bid_price
}

export const calcPageCount = (totalCount, perPage) => {
 return Math.floor( totalCount /perPage)+(totalCount  %  perPage  > 0 ? 1 : 0) 
}
