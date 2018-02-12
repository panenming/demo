import tensorflow as tf
import numpy as np
import train1
import time
import cv2

def crack_captcha(output,sess,captcha_image,dz):
	"""
	使用模型做预测
	Parameters:
		captcha_image:数据
		captcha_label:标签
	"""
	img = captcha_image.flatten()
	predict = tf.argmax(tf.reshape(output, [-1, dz.max_captcha, dz.char_set_len]), 2)
	text_list = sess.run(predict, feed_dict={dz.X: [img], dz.keep_prob: 1})
	text = text_list[0].tolist()
	vector = np.zeros(dz.max_captcha*dz.char_set_len)
	i = 0
	for n in text:
		vector[i*dz.char_set_len + n] = 1
		i += 1
	prediction_text = dz.vec2text(vector)
	# print("预测: ",prediction_text)
	return prediction_text

def autoCheck(name,dz,sess,output):
	# start = time.time()
	img = np.mean(cv2.imread(name), -1)
	txt = crack_captcha(output,sess,img.flatten() / 255,dz)
	# end = time.time()
	# print("用时：", end-start)
	return txt

if __name__ == '__main__':
	dz = train1.Train()
	batch_x, batch_y = dz.get_next_batch(False, 5)
	print("正确: ",dz.vec2text(batch_y[0]))
	output = dz.crack_captcha_cnn()
	saver = tf.train.Saver()
	sess =  tf.Session()
	saver.restore(sess, tf.train.latest_checkpoint('pet-chain/model/'))
	start = time.time()
	crack_captcha(output,sess,batch_x[0],dz)
	end = time.time()
	print("用时：", end-start)