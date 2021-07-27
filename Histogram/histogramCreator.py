from matplotlib import pyplot as plt
import skimage.io
import skimage.color
file = ()
image = skimage.io.imread(file)

transperancy = float(0.5)
plt.xlabel('Intensity Value')
plt.ylabel('Count')

plt.hist(image.ravel(), bins = 128, color = 'grey', alpha = 0.5)
plt.hist(image[:, :, 0].ravel(), bins = 128, color = 'red', alpha = transperancy)
plt.hist(image[:, :, 1].ravel(), bins = 128, color = 'Green', alpha = transperancy)
plt.hist(image[:, :, 2].ravel(), bins = 128, color = 'Blue', alpha = transperancy)

plt.legend(['Total', 'Red', 'Green', 'Blue'])
plt.show()