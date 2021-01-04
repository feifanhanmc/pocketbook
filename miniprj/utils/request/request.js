// 同时发送异步代码的次数
let ajaxTimes=0;
export const request=(params)=>{
  let header={...params.header};
  // 拼接header 带上token，即：acc_user
  header["Authorization"]=wx.getStorageSync("acc_user");

  
  ajaxTimes++;
  // 显示加载中 效果
  wx.showLoading({
    title: "加载中",
    mask: true
  });
    

  // 定义公共的url
  const baseUrl="https://sun.liuyihua.com";
  return new Promise((resolve,reject)=>{
    wx.request({
     ...params,
     header:header,
     url:baseUrl+params.url,
     success:(result)=>{
       resolve(result.data.data);
     },
     fail:(err)=>{
       reject(err);
     },
     complete:()=>{
      ajaxTimes--;
      if(ajaxTimes===0){
        //  关闭正在等待的图标
        wx.hideLoading();
      }
     }
    });
  })
}